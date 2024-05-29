library(dplyr)
library(spdep)
library(scanstatistics)
library(ggplot2)
library(tidyr)
library(readxl)
library(sp)
library(magrittr)
library(terra)
library(sf)

# setwd('D:/Dropbox/2022/2022 ASF/code/code/Ko/')
# window_path <- "D:/Dropbox/2022/2022 ASF/1차정리_202307/Data/시군구별 데이터/통합_shp/"
apple_path <- "/Users/gogyeongtae/Library/CloudStorage/Dropbox/2022/2022 ASF/1차정리_202307/Data/시군구별 데이터/통합_shp/"

################
# Data
shp <- st_read(paste0(apple_path, 'shp통합4.shp'))

# shp <- readOGR(dsn = window_path, layer = rgdal::ogrListLayers(window_path)[endsWith(rgdal::ogrListLayers(window_path), '4')][3])
coord <- read_excel(paste0(apple_path, '시군구위도경도.xlsx'))

# 확진시간.csv는 행정구역별로 월별 폐사체 수를 나타내는 공간 패널 데이터이다.
used_data <- read.csv('../Data/data_carcass.csv', header = TRUE)

################
used_data$time <- as.Date(used_data$time)
used_data$time <- format(used_data$time, '%Y%m')
used_data$time <- as.numeric(used_data$time)

used_data$distance <- exp(-1 * used_data$distance)


used_data <- used_data[,c('time', 'SIG_CD', 'distance', 
                          'forest', 'season', 'x', 'y', 'total')]
used_data$total <- round(used_data$total)
used_data$distance2 <- used_data$distance^2
used_data$distance3 <- used_data$distance^3

# First period 
counts <- used_data %>%
  filter(time >= 202209 & time <= 202212) %>% 
  df_to_matrix(time_col = 'time', location_col = 'SIG_CD', value_col = 'total')

used_data %>%
  filter(time >= 202209 & time <= 202212) %>% 
  filter(SIG_CD==47930)

zones <- shp %>%
  as.data.frame() %>%
  dplyr::select(x,y) %>%
  as.matrix %>%
  spDists(x = ., y = ., longlat = TRUE) %>%
  dist_to_knn(k=3) %>%
  knn_zones

used_data$time_num <- rep( seq(1, 43, 1), 250)

## Poisson
mod = glm(round(total) ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
          data = used_data %>% filter(time < 202209),
          family = poisson(link = 'log'))
summary(mod)

# data <- used_data %>% filter(time < 202209)
# pois_log_likelihood <- function(log_mu_intercept, log_mu_X1, log_mu_X2, log_mu_X3) {
#   mu <- exp(log_mu_intercept + log_mu_X1 * data$distance + log_mu_X2 * data$season + log_mu_X3 * data$time_num +
#               log(data$forest))
#   -sum(dpois(data$total, lambda = mu, log = TRUE))
# }
# start_values <- list(log_mu_intercept = 0, log_mu_X1 = 0, log_mu_X2 = 0, log_mu_X3 = 0)
# pois_model <- mle2(pois_log_likelihood, start = start_values)
# summary(pois_model)

ebp_baselines <- used_data %>%
  filter(time >= 202209 & time <= 202212) %>%
  mutate(mu = predict(mod, newdata = ., type = 'response')) %>%
  scanstatistics::df_to_matrix(time_col = 'SIG_CD', 
                               location_col = 'time',
                               value_col = 'mu') %>% t()

MC.count <- 999
poisson_result <- scan_eb_poisson(counts = counts,
                                  zones = zones,
                                  baselines = ebp_baselines,
                                  n_mcsim = MC.count)

ps_cluster.1 <- top_clusters(poisson_result, zones, k = 10, overlapping = FALSE)

# NB model
library(MASS)
mod2 <- glm.nb(round(total) ~  offset(log(forest))  + distance + distance2 + distance3 + season + time_num,
           data = used_data %>% filter(time < 202209), init.theta = 1, link = 'log')

summary(mod2)

ebp_baselines2 <- used_data %>%
  filter(time >= 202209 & time <= 202212) %>%
  mutate(mu = predict(mod2, newdata = ., type = 'response')) %>%
  scanstatistics::df_to_matrix(time_col = 'SIG_CD', 
                               location_col = 'time',
                               value_col = 'mu') %>% t()

nb_result <- scan_eb_negbin(counts = counts,
                            zones = zones,
                            baselines = ebp_baselines2,
                            n_mcsim = 5000)

nb_cluster.1 <- top_clusters(nb_result, zones, k = 10)

## ZIP model
library(pscl)

mod3 <- zeroinfl(round(total) ~ offset(log(forest)) + distance + I(distance^2) + I(distance^3) + season + time_num,
                 data = used_data %>% filter(time < 202209))
mod3$dist
summary(mod3)

ebp_baselines3 <- used_data %>%
  filter(time >= 202209 & time <= 202212) %>%
  mutate(mu = predict(mod3, newdata = ., type = 'response')) %>%
  scanstatistics::df_to_matrix(time_col = 'SIG_CD', 
                               location_col = 'time',
                               value_col = 'mu') %>% t()

used_data %>%
  filter(time <= 202212) %>%
  mutate(mu = predict(mod, newdata = ., type = 'response'))  %>%
  filter(SIG_CD==43130)

used_data %>%
  filter(time >= 202209 & time <= 202212) %>%
  mutate(mu = predict(mod2, newdata = ., type = 'response'))  %>%
  filter(SIG_CD==43130)

used_data %>%
  filter(time >= 202209 & time <= 202212) %>%
  mutate(mu = predict(mod3, newdata = ., type = 'response'))  %>%
  filter(SIG_CD==43130)

zf_result <- scan_eb_zip(counts = counts,
                         zones = zones,
                         baselines = ebp_baselines3,
                         n_mcsim = 5000)

zf_cluster.1 <- top_clusters(zf_result, zones, k = 10, overlapping = FALSE)

scan_result <- scan_permutation(counts = counts, 
                                zones = zones, 
                                n_mcsim = 999)

scan_cluster.1 <- top_clusters(scan_result, zones, k = 3, overlapping = FALSE)

######################
# Second period

counts <- used_data %>%
  filter(time >= 202301 & time <= 202304) %>% 
  df_to_matrix(time_col = 'time', location_col = 'SIG_CD', value_col = 'total')

merge_df <- merge(shp, coord, id='SIG_CD')
names(merge_df)

## Poisson
mod = glm(total ~ offset(log(forest)) + 1 + distance + I(distance^2) + I(distance^3) + season + time_num,
          data = used_data %>% filter(time < 202301),
          family = poisson(link = 'log'))
summary(mod)

ebp_baselines <- used_data %>%
  filter(time >= 202301 & time <= 202304) %>%
  mutate(mu = predict(mod, newdata = ., type = 'response')) %>%
  scanstatistics::df_to_matrix(time_col = 'SIG_CD', 
                               location_col = 'time',
                               value_col = 'mu') %>% t()

MC.count <- 999
poisson_result <- scan_eb_poisson(counts = counts,
                                  zones = zones,
                                  baselines = ebp_baselines,
                                  n_mcsim = 999)

ps_cluster.1 <- top_clusters(poisson_result, zones, k = 10, overlapping = FALSE)

# NB model
library(MASS)
mod2 <- glm.nb(total ~  offset(log(forest)) + season + distance + I(distance^2)+ I(distance^3) + time_num,
               data = used_data %>% filter(time < 202301), init.theta = 0.5)
summary(mod2)

ebp_baselines2 <- used_data %>%
  filter(time >= 202301 & time <= 202304) %>%
  mutate(mu = predict(mod2, newdata = ., type = 'response')) %>%
  scanstatistics::df_to_matrix(time_col = 'SIG_CD', 
                               location_col = 'time',
                               value_col = 'mu') %>% t()

nb_result <- scan_eb_negbin(counts = counts,
                            zones = zones,
                            baselines = ebp_baselines2,
                            n_mcsim = 999)

nb_cluster.1 <- top_clusters(nb_result, zones, k = 10, overlapping = FALSE)

## ZIP model
library(pscl)
mod3 <- zeroinfl(total ~  offset(log(forest)) + season + distance + I(distance^2) + I(distance^3) + time_num,
                 data = used_data %>% filter(time < 202301))
summary(mod3)

ebp_baselines3 <- used_data %>%
  filter(time >= 202301 & time <= 202304) %>%
  mutate(mu = predict(mod3, newdata = ., type = 'response')) %>%
  scanstatistics::df_to_matrix(time_col = 'SIG_CD', 
                               location_col = 'time',
                               value_col = 'mu') %>% t()

zf_result <- scan_eb_zip(counts = counts,
                         zones = zones,
                         baselines = ebp_baselines3,
                         n_mcsim = 99)

zf_cluster.1 <- top_clusters(zf_result, zones, k = 10, overlapping = FALSE)

AIC(mod); AIC(mod2); AIC(mod3)
