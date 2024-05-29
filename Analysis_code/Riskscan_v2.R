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


apple_path <- "/Users/gogyeongtae/Library/CloudStorage/Dropbox/2022/2022 ASF/1차정리_202307/Data/시군구별 데이터/통합_shp/"

# Data
shp <- st_read(paste0(apple_path, 'shp통합4.shp'))
coord <- read_excel(paste0(apple_path, '시군구위도경도.xlsx'))
data <- read.csv('./result.csv', header = TRUE)
used_data <- read.csv('../Data/data_carcass.csv', header = TRUE)

used_data$time <- as.Date(used_data$time)
used_data$time <- format(used_data$time, '%Y%m')
used_data$time <- as.numeric(used_data$time)

used_data$distance <- exp(-1 * used_data$distance)

####################
a1 <- used_data %>% group_by(time) %>% summarise(total = sum(total)) %>% round()
b1 <- used_data %>% group_by(time) %>% summarise(NUMPOINTS = sum(NUMPOINTS)) %>% round()

plot(b1$NUMPOINTS, type = 'o', col = 'red')
lines(a1$total, type = 'o')
####################

used_data <- used_data[,c('time', 'SIG_CD', 'distance', 
                          'forest', 'season', 'x', 'y', 'total')]
used_data$total <- round(used_data$total)
used_data$distance2 <- used_data$distance^2
used_data$distance3 <- used_data$distance^3
used_data$time_num <- rep( seq(1, 43, 1), 250)

mod = glm(round(total) ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
          data = used_data %>% filter(time < 202209),
          family = poisson(link = 'log'))

pred <- predict(mod, newdata = used_data %>% filter(time >= 202209 & time <= 202212), type = 'response')
true <- used_data$total[used_data$time >= 202209 & used_data$time <= 202212]
plot(true, pred, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'green')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'red', lwd = 2)
legend('topright', legend = c('Poisson'), col = c('green'), pch = 17)

library(MASS)
mod2 = glm.nb(round(total) ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
          data = used_data %>% filter(time < 202209))

pred2 <- predict(mod2, newdata = used_data %>% filter(time >= 202209 & time <= 202212), type = 'response')
true2 <- used_data$total[used_data$time >= 202209 & used_data$time <= 202212]
plot(true2, pred2, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'red')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'red', lwd = 2)
legend('topright', legend = c('Negative Binomial'), col = c('red'), pch = 17)

library(pscl)
mod3 = hurdle(total ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
          data = used_data %>% filter(time < 202209),
          dist = 'poisson', zero.dist = 'binomial')

pred3 <- predict(mod3, newdata = used_data %>% filter(time >= 202209 & time <= 202212), type = 'response')
true3 <- used_data$total[used_data$time >= 202209 & used_data$time <= 202212]
plot(true3, pred3, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'blue')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'red', lwd = 2)
legend('topright', legend = c('ZIP'), col = c('blue'), pch = 17)

plot(true, pred, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'green')
points(true2, pred2, pch = 17, col = 'red')
points(true3, pred3, pch = 17, col = 'blue')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'black', lwd = 2)
legend('topright', legend = c('Poisson', 'Negative Binomial', 'ZIP'), col = c('green', 'red', 'blue'), pch = 17)

############################################################################################################
pred <- predict(mod, newdata = used_data %>% filter(time <= 202209 ), type = 'response')
true <- used_data$total[used_data$time <= 202209 ]
plot(true, pred, pch = 17, ylim = c(0, 10), xlim = c(0, 10))
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'red', lwd = 2)

library(MASS)
mod2 = glm.nb(round(total) ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
              data = used_data %>% filter(time < 202209))

pred2 <- predict(mod2, newdata = used_data %>% filter(time <= 202209), type = 'response')
true2 <- used_data$total[used_data$time <= 202209 ]
plot(true2, pred2, pch = 17, ylim = c(0, 10), xlim = c(0, 10))
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'red', lwd = 2)

library(pscl)
mod3 = hurdle(total ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
              data = used_data %>% filter(time < 202209),
              dist = 'poisson', zero.dist = 'binomial')

pred3 <- predict(mod3, newdata = used_data %>% filter(time <= 202209), type = 'response')
true3 <- used_data$total[used_data$time <= 202209]
plot(true3, pred3, pch = 17, ylim = c(0, 10), xlim = c(0, 10))
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'red', lwd = 2)

plot(true, pred, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'green')
points(true2, pred2, pch = 17, col = 'red')
points(true3, pred3, pch = 17, col = 'blue')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'black', lwd = 2)
legend('topright', legend = c('Poisson', 'Negative Binomial', 'ZIP'), col = c('green', 'red', 'blue'), pch = 17)

# Fitting residual for machine learning
residual <- used_data %>% filter(time <= 202209) %>% dplyr::select(total) - predict(mod, newdata = used_data %>% filter(time <= 202209), type = 'response')
residual2 <- used_data %>% filter(time <= 202209) %>% dplyr::select(total) - predict(mod2, newdata = used_data %>% filter(time <= 202209), type = 'response')
residual3 <- used_data %>% filter(time <= 202209) %>% dplyr::select(total) - predict(mod3, newdata = used_data %>% filter(time <= 202209), type = 'response')

data <- used_data %>% filter(time <= 202209)
data['residual'] <- residual
data['residual2'] <- residual2
data['residual3'] <- residual3

library(randomForest)
rf <- randomForest(residual ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
                   data = data)
rf2 <- randomForest(residual2 ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
                   data = data)
rf3 <- randomForest(residual3 ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
                   data = data)

pred_rf <- predict(rf3, newdata = used_data %>% filter(time >= 202209 & time <= 202212))
true_rf <- data$total[used_data$time >= 202209 & used_data$time <= 202212] - predict(mod, newdata = used_data %>% filter(time >= 202209 & time <= 202212), type = 'response')

plot(true_rf, pred_rf, pch = 17, ylim = c(-10, 10), xlim = c(-10, 10))
lines(seq(-10,10,0.1), seq(-10,10,0.1), lty = 2, col = 'red', lwd = 2)

plot(true, pred, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'green')
points(true, pred + pred_rf, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'red')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'black', lwd = 2)


############################################################################################################

mod = glm(round(total) ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num ,
          data = used_data %>% filter(time <= 202212),
          family = poisson(link = 'log'))

pred <- predict(mod, newdata = used_data %>% filter(time >= 202301 & time <= 202305), type = 'response')
true <- used_data$total[used_data$time >= 202301 & used_data$time <= 202305]
plot(true, pred, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'green')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'red', lwd = 2)
legend('topright', legend = c('Poisson'), col = c('green'), pch = 17)

library(MASS)
mod2 = glm.nb(round(total) ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
              data = used_data %>% filter(time < 202209))

pred2 <- predict(mod2, newdata = used_data %>% filter(time >= 202301 & time <= 202305), type = 'response')
true2 <- used_data$total[used_data$time >= 202301 & used_data$time <= 202305]
plot(true2, pred2, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'red')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'red', lwd = 2)
legend('topright', legend = c('Negative Binomial'), col = c('red'), pch = 17)

library(pscl)
mod3 = hurdle(total ~ offset(log(forest)) + 1  + distance + distance2 + distance3 + season + time_num,
              data = used_data %>% filter(time < 202209),
              dist = 'poisson', zero.dist = 'binomial')

pred3 <- predict(mod3, newdata = used_data %>% filter(time >= 202301 & time <= 202305), type = 'response')
true3 <- used_data$total[used_data$time >= 202301 & used_data$time <= 202305]
plot(true3, pred3, pch = 17, ylim = c(0, 10), xlim = c(0, 10), col = 'blue')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'red', lwd = 2)
legend('topright', legend = c('ZIP'), col = c('blue'), pch = 17)

plot(true, pred, pch = 17,  col = 'green')
points(true2, pred2, pch = 17, col = 'red')
points(true3, pred3, pch = 17, col = 'blue')
lines(seq(0,10,0.1), seq(0,10,0.1), lty = 2, col = 'black', lwd = 2)
legend('topright', legend = c('Poisson', 'Negative Binomial', 'ZIP'), col = c('green', 'red', 'blue'), pch = 17)




######################
data1 <- used_data %>%
  group_by(time) %>%
  summarise(total = sum(total))

phase1 <- which(data1$time >= 202209 & data1$time <= 202212)
phase2 <- which(data1$time >= 202301 & data1$time < 202305)

plot(data1$total, type = 'h', lwd = 5, col = 'gray', ylab = 'total', xlab = 'time')
abline(v = phase1[1], col = 'red', lty = 2)
abline(v = phase1[length(phase1)], col = 'red', lty = 2)
abline(v = phase2[1], col = 'blue', lty = 2)
abline(v = phase2[length(phase2)], col = 'blue', lty = 2)

data1[phase1,]
data1[phase2,]


