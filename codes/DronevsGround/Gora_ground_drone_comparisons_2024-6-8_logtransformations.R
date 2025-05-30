#Compare Raquel data with ground-data from the lightning strikes
#Begin script on Nov. 12, 2021 and edits continued until June 8, 2024

#Primary objectives:
### Test how well canopy gap area or depth predict major lightning damage characteristics
## 1. trees damaged, 2. trees killed, 3. biomass loss, and 4. disturbed area
##### Do this first part with final ground census and closest airborn census
### If possible, compare the temporal trends as well

#open packages
library(ggplot2)
library(dplyr)
library(car)
library(egg)
library(gridExtra)
library(extrafont)
loadfonts(device="win")

#clear workspace
rm(list=ls())

#set working directory
setwd("G:/My Drive/collaborations/Raquel_Araujo/figures")

#import that datsets for time-to-strike
timetolastimage <- read.csv("G:/My Drive/collaborations/Raquel_Araujo/new_data/taballstrikes_timetolastimage.csv", row.names = 1)
str(timetolastimage)
timetolastimage$survey.days.post.strike <- timetolastimage$diflastimg*(365.25/12)
length(unique(timetolastimage$nstrike))#these data only include 15 strikes

#load data
drone_data_inter <- read.csv("G:/My Drive/collaborations/Raquel_Araujo/new_data/tab_strikes_area_hdrop_volume.csv", row.names = 1)
str(drone_data_inter)
summary(is.na(drone_data_inter))

#combine the timeframe data with the drone_data
drone_data <- full_join(drone_data_inter,timetolastimage)
summary(is.na(drone_data))#a few NA values inserted where no canopy gap was identified

#create canopy gap identifier column and replace NA with 0
drone_data$gap_binary <- ifelse(is.na(drone_data$area),"nogap","gap")
drone_data$area[is.na(drone_data$area)]<-0
drone_data$meanHD[is.na(drone_data$meanHD)]<-0
drone_data$meanHDp[is.na(drone_data$meanHDp)]<-0
drone_data$volume[is.na(drone_data$volume)]<-0

#change column name
colnames(drone_data)[2] <- "strike"

#load
load("G:/My Drive/collaborations/Raquel_Araujo/strike_data/regression_covariates.Rdata")
str(regression_covariates)

#trim the regression covariates to only include the relevant strikes
focal_strikes <- unique(drone_data$strike)
regression_covariates_trim <- regression_covariates[regression_covariates$strike %in% focal_strikes,]

#create the basic ggplot theme
theme_basis<-theme(axis.title = element_text(family = "Arial", color="black", face="bold", size=14))+
  theme(axis.text=element_text(family = "Arial",colour="black", face ="bold", size = 12)) +
  theme(legend.text=element_text(family = "Arial",colour="black", face ="bold", size = 10)) +
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        panel.background = element_blank(),axis.line = element_line(colour = "black"),
        axis.ticks = element_line(colour="black")) +
  theme(legend.background = element_blank())

############################################################
### -- Calculate days since strike for the drone data -- ###
############################################################
# #import all strike data and subset the first row
# lightning_data <- read.csv("G:/My Drive/Lightning/Data_Management_lightning/cleaned_data/cleaned_2015-2020_lightningcensuses.csv", row.names=1)
# lightning_data_days <- lightning_data[,c("strike","Strike.date")] %>% 
#   group_by(strike) %>%  slice(1)
# 
# #drop unncessary strikes
# lightning_data_days_trim <- lightning_data_days[lightning_data_days$strike %in% focal_strikes,]
# str(lightning_data_days_trim)
# 
# #add strike date to the drone_data dataframe
# drone_data2 <- left_join(drone_data,lightning_data_days_trim, by = "strike")

#now calculate days post-strike for each measurement
drone_data$Strike.date <- as.Date(drone_data$datestrike,"%Y-%m-%d")
drone_data$drone.date <- as.Date(drone_data$date,"%Y-%m-%d")

drone_data$days.post.strike <- as.numeric(difftime(drone_data$drone.date,drone_data$Strike.date))
drone_data$days.post.strike_w0 <- ifelse(is.na(drone_data$days.post.strike),0,drone_data$days.post.strike)
str(drone_data)

#what is the date of first gap creation for each strike?
first_gap <- drone_data %>% group_by(strike) %>% 
  arrange(days.post.strike) %>% slice(1)
nrow(first_gap);length(unique(first_gap$strike))#confirm 1 row per strike
mean(first_gap$days.post.strike,na.rm=T);sd(first_gap$days.post.strike,na.rm=T)
min(first_gap$days.post.strike,na.rm=T);max(first_gap$days.post.strike,na.rm=T)

#plot gap area, volume, and depth over time for strikes
ggplot(drone_data,aes(x = days.post.strike_w0, y = area)) +
  geom_line() + geom_point() + facet_wrap(~strike)

#calculate cumulative area and cumulative volume

drone_data <- drone_data %>%
  group_by(strike) %>%
  arrange(days.post.strike,.by_group = T) %>%
  mutate(cumulative_area = cumsum(area),
         cumulative_vol = cumsum(volume))

##################################################################
### -- Does gap area or volume typically increase with time -- ###
##################################################################
str(drone_data)

#create new df for this estimate
drone_data_peak_inter <- drone_data

#create 'max area' column
drone_data_peak <- drone_data_peak_inter %>%
  group_by(strike) %>%
  mutate(max_area = max(cumulative_area)) %>%
  filter(cumulative_area == max_area)
# str(drone_data_peak)
nrow(drone_data_peak);length(unique(drone_data_peak$strike))

#plot peak area versus time of measurement
days_to_reach_max_gaparea <- ggplot(drone_data_peak,aes(x = days.post.strike_w0, y = cumulative_area)) +
  geom_point(position = position_jitter(width=40)) + 
  theme_basis + coord_cartesian(ylim = c(-10,800)) +
  geom_smooth(method = "lm",color = "black") +
  scale_y_continuous(expression(bold("Maximum gap area"~(m^{2}))),expand = c(0,0)) +
  scale_x_continuous("Days to reach maximum area",expand = c(0,3))

days_to_reach_max_gaparea

# ggsave("days_to_reach_max_gaparea.tiff",dpi = 600, compression = "lzw",
#        width = 3.25, height = 1.8, scale = 1.8)

days_to_reach_max_gaparea_col <- ggplot(drone_data_peak,aes(x = days.post.strike_w0, y = cumulative_area)) +
  geom_point(aes(color = survey.days.post.strike),position = position_jitter(width=40)) + 
  theme_basis + coord_cartesian(ylim = c(-10,800)) +
  theme(legend.position = c(.15,.7)) +
  theme(legend.title=element_text(family = "Arial",colour="black", face ="bold", size = 12)) +
  geom_smooth(method = "lm",color = "black") +
  scale_color_gradient(low = "blue",high = "gold2", name = "Days monitored") +
  scale_y_continuous(expression(bold("Maximum gap area"~(m^{2}))),expand = c(0,0)) +
  scale_x_continuous("Days to reach maximum area",expand = c(0,3))

days_to_reach_max_gaparea_col

# ggsave("days_to_reach_max_gaparea_col.tiff",dpi = 600, compression = "lzw",
#        width = 3.25, height = 1.8, scale = 1.8)

#days of surveying versus gap area
surveydays_v_gaparea <- ggplot(drone_data_peak,aes(x = survey.days.post.strike, y = cumulative_area)) +
  geom_point() + 
  theme_basis + coord_cartesian(ylim = c(-10,800)) +
  geom_smooth(method = "lm",color = "black") +
  scale_color_gradient(low = "blue",high = "gold2") +
  scale_y_continuous(expression(bold("Maximum gap area"~(m^{2}))),expand = c(0,0)) +
  scale_x_continuous("Total survey duration (days)",expand = c(0,10))

surveydays_v_gaparea

# ggsave("surveydays_v_gaparea.tiff",dpi = 600, compression = "lzw",
#        width = 3.25, height = 1.8, scale = 1.8)
getwd()

#create combined plot
surveydays_v_gaparea_nolab <- surveydays_v_gaparea + scale_y_continuous(name = element_blank(),expand = c(0,0))


gap_area_time_comb <- ggarrange(days_to_reach_max_gaparea,surveydays_v_gaparea_nolab,
                      ncol = 2, labels = c("a","b"))

# ggsave("gap_area_time_comb.tiff",gap_area_time_comb,width = 6.5,height = 2,dpi = 600,
#        scale=1.6,compression="lzw")
# ggsave("gap_area_time_comb.png",gap_area_time_comb,width = 6.5,height = 2,dpi = 600,
#        scale=1.6)
getwd()


#test for significant relationships
# total area versus total survey time
gap_v_time_mod <- lm(cumulative_area~survey.days.post.strike, data = drone_data_peak)
summary(gap_v_time_mod)#decent residuals
plot(gap_v_time_mod)

#total area versus the time until peak area was observed
gap_v_timetopeak_mod <- lm(cumulative_area~days.post.strike_w0, data = drone_data_peak)
summary(gap_v_timetopeak_mod)
plot(gap_v_timetopeak_mod)#Mediocre residuals

#how much time did it take for gaps to peak, on average?
mean(drone_data_peak$days.post.strike,na.rm=T);sd(drone_data_peak$days.post.strike,na.rm=T)
mean(drone_data_peak$days.post.strike[drone_data_peak$survey.days.post.strike>365],na.rm=T)

#how much time did it take for any strike to reach peak gap area?
mean(drone_data_peak$days.post.strike_w0)
mean(drone_data_peak$days.post.strike_w0[drone_data_peak$survey.days.post.strike>365])
sd(drone_data_peak$days.post.strike_w0[drone_data_peak$survey.days.post.strike>365])

#####################################################
### -- Calculate average gap area with 95% CIs -- ###
#####################################################

resampled_allstrikes <- rep(NA,1000)
for(i in 1:1000){
  resampled_allstrikes[i] <- mean(sample(drone_data_peak$cumulative_area,
                                    nrow(drone_data_peak),replace = T))
}
mean(drone_data_peak$cumulative_area)
quantile(resampled_allstrikes,0.025)
quantile(resampled_allstrikes,0.975)

resampled_allgaps <- rep(NA,1000)
for(i in 1:1000){
  resampled_allgaps[i] <- mean(sample(drone_data_peak$cumulative_area[drone_data_peak$cumulative_area!=0],
                                         nrow(drone_data_peak[drone_data_peak$cumulative_area!=0,]),replace = T))
}
mean(drone_data_peak$cumulative_area[drone_data_peak$cumulative_area!=0])
quantile(resampled_allgaps,0.025)
quantile(resampled_allgaps,0.975)



##################################################################
### -- Compare the timing and total samples of each dataset -- ###
##################################################################

#create strike date dataframe from the full-strike data

#how many time points do we have for each dataset?
sum_covars <- regression_covariates_trim %>%
  group_by(strike) %>%
  summarise(covar_samples = length(strike),
            earliest_ground = min(days.post.strike),
            latest_ground = max(days.post.strike)) 

sum_drone <- drone_data %>%
  group_by(strike) %>%
  summarise(drone_samples = length(strike),
            earliest_drone = min(days.post.strike_w0),
            latest_drone = max(days.post.strike_w0)) 

#combine files
combined_files <- left_join(sum_covars,sum_drone, by = "strike")
# View(combined_files)

#calculate the difference in combined files and then view this
combined_files$sample_diff <- combined_files$covar_samples - combined_files$drone_samples
# View(combined_files)

###########################################################################
### -- associate final ground data with nearest drone data (in time) -- ###
###########################################################################
#select the final ground census of each strike
final_ground <- regression_covariates_trim %>%
  group_by(strike) %>%
  arrange(desc(days.post.strike), .by_group = T) %>%
  slice(1)
hist(final_ground$days.post.strike)

#add the days.post.strike for each strike to all of the drone data
ground_survey_days <- final_ground[,c("strike","days.post.strike")]
str(ground_survey_days)
colnames(ground_survey_days)[2]<-"ground.days.post.strike"

drone_data_inter <- left_join(drone_data,ground_survey_days)
str(drone_data_inter)

#subtract days post strike from the final ground survey days
drone_data_inter$final.ground.moredays <- drone_data_inter$ground.days.post.strike-drone_data_inter$days.post.strike
drone_data_inter$diff.final.ground.days <- abs(drone_data_inter$days.post.strike-drone_data_inter$ground.days.post.strike)

#select the drone data with the least time mismatch
drone_data_match <- drone_data_inter %>%
  group_by(strike) %>%
  arrange(diff.final.ground.days, .by_group = T) %>%
  slice(1) 
hist(drone_data_match$diff.final.ground.days)

#plot the difference in time as a function of the timing of the ground survey
#create a strike year column
library(stringr)
drone_data_match$StrikeYear<-NA
for(i in 1:nrow(drone_data_match)){
  drone_data_match$StrikeYear[i] <- str_split(drone_data_match$datestrike[i],"-")[[1]][1]
}
# 
# #now plot the data
# survey_date_comparisons <- ggplot(drone_data_match, aes(x = ground.days.post.strike,y = final.ground.moredays)) +
#   geom_point(aes(color = StrikeYear)) + theme_basis +
#   scale_x_continuous("Days post-strike - last ground survey (days)", breaks = seq(200,800,100),
#                      limits = c(300,820), labels = c("200","300","400","500","600","700","800"),
#                      expand = c(0,0)) +
#   scale_y_continuous("Last ground survey date minus\n closest drone survey date (days)", breaks = seq(-200,800,100),
#                      limits = c(-200,650), labels = c("-200","","0","","200","","400","","600","","800"),
#                      expand = c(0,0)) +
#   theme(legend.position = c(.12,.85),legend.background = element_blank(),legend.key = element_blank(),
#         legend.key.height = unit(.3,"cm"),
#         legend.text = element_text(family = "Arial", face = "bold",size = 10),
#         legend.title = element_text(family = "Arial", face = "bold",size = 12))
# 
# survey_date_comparisons
# 
# # ggsave("survey_date_comparisons.tiff",survey_date_comparisons,compression = "lzw",
# #        scale = 1.8, height = 2, width = 3.25)

#combine the final ground surveys with these drone data
final_ground_wdrone <- left_join(drone_data_match,final_ground,by = "strike")
str(final_ground_wdrone)

#now plot the data
survey_time_comparisons <- ggplot(final_ground_wdrone, aes(x = survey.days.post.strike,y = ground.days.post.strike)) +
  geom_point(aes(color = StrikeYear), shape = 1, position = position_jitter(width = 20, height = 15)) + theme_basis +
  scale_y_continuous("Duration of ground surveys (days)", breaks = seq(200,800,100),
                     limits = c(300,930), labels = c("200","300","400","500","600","700","800"),
                     expand = c(0,0)) +
  scale_x_continuous("Duration of drone surveys (days)", breaks = seq(0,1750,250),
                     limits = c(0,1750), labels = c("0","","500","","1,000","","1,500",""),
                     expand = c(0,0)) +
  theme(legend.position = c(.085,.87),legend.background = element_blank(),legend.key = element_blank(),
        legend.key.height = unit(.3,"cm"),
        legend.text = element_text(family = "Arial", face = "bold",size = 10),
        legend.title = element_text(family = "Arial", face = "bold",size = 12))

survey_time_comparisons

ggsave("survey_time_comparisons.tiff",survey_time_comparisons,compression = "lzw",
       scale = 1.8, height = 2, width = 3.25)
ggsave("survey_time_comparisons.png",survey_time_comparisons,
       scale = 1.8, height = 2, width = 3.25)

################################################
### -- Plot the data as a continuous line -- ###
################################################
all_measures <- bind_rows(regression_covariates_trim,drone_data)
str(all_measures)

#create a for loop specifying how to propogate values forward
all_measures$days.post.strike<-ifelse(is.na(all_measures$days.post.strike),0,all_measures$days.post.strike)
all_measures_ordered <- all_measures %>%
  group_by(strike) %>%
  arrange(days.post.strike, .by_group = T)

#create vectors to define whether there is a change-point
all_measures_ordered$changepoints <- ifelse(is.na(all_measures_ordered$total_necromass_kg)&
                                              is.na(all_measures_ordered$cumulative_area),"Both",
                                            ifelse(is.na(all_measures_ordered$total_necromass_kg)&
                                                     !is.na(all_measures_ordered$cumulative_area),"Drone",
                                                   ifelse(!is.na(all_measures_ordered$total_necromass_kg)&
                                                            is.na(all_measures_ordered$cumulative_area),"Ground",NA)))

#create a for-loop to propagate missing values forward
for(j in 1:length(unique(all_measures_ordered$strike))){
  strike_list <- unique(all_measures_ordered$strike)
  inter_df <- all_measures_ordered[all_measures_ordered$strike==strike_list[j],]
  for(i in 1:nrow(inter_df)){
    if(i==1&is.na(inter_df$total_necromass_kg[i])){
      inter_df_noNA <- inter_df[!is.na(inter_df$total_necromass_kg),]
      inter_df[i,3:24] <- inter_df_noNA[1,3:24]
    }
    if(i==1&is.na(inter_df$cumulative_area[i])){
      inter_df_noNA <- inter_df[!is.na(inter_df$cumulative_area),]
      inter_df[i,25:39] <- inter_df_noNA[1,25:39]
    }
    if(is.na(inter_df$total_necromass_kg[i])){
      inter_df[i,3:24] <- inter_df[i-1,3:24]
    }
    if(is.na(inter_df$cumulative_area[i])){
      inter_df[i,25:39] <- inter_df[i-1,25:39]
    }
    all_measures_ordered[all_measures_ordered$strike==strike_list[j],]<-inter_df
  }
  
}

summary(all_measures_ordered)

#now rescale values of necromass and cumulative area to 0-1
all_measures_ordered$scaled_area <- all_measures_ordered$cumulative_area/max(all_measures_ordered$cumulative_area)
all_measures_ordered$scaled_necromass <- all_measures_ordered$total_necromass_kg/max(all_measures_ordered$total_necromass_kg)
hist(all_measures_ordered$scaled_area)
hist(all_measures_ordered$scaled_necromass)

#create figure breaks and labels
labels_area <- seq(0,800,200)
breaks_area <- seq(0,800,200)/max(all_measures_ordered$cumulative_area)
labels_necromass <- (seq(0,40000,10000)/1000)
breaks_necromass <- (seq(0,40000,10000)/1000)/max(all_measures_ordered$total_necromass_kg/1000)

#create a test figure with two axes
test_df <- all_measures_ordered[all_measures_ordered$strike=="12",]

#create a figure
ggplot(test_df,aes(x = days.post.strike,y = scaled_area), color = "red") +
  geom_line() + theme_basis +
  geom_line(aes(x = days.post.strike, y = scaled_necromass), color = "blue")

faceted_gaparea_by_biomass <- ggplot(all_measures_ordered,aes(x = days.post.strike,y = scaled_area)) +
  geom_line(color = "red") + theme_basis +
  geom_line(aes(x = days.post.strike, y = scaled_necromass), color = "blue") +
  facet_wrap(~strike,ncol = 5) + 
  scale_x_continuous(name = "Time post-strike (days)")+
  scale_y_continuous(name = expression(bold("Canopy gap area"~(m^{2}))),breaks = breaks_area,
                     labels = labels_area,
                     sec.axis = sec_axis(~.*1,name = "Dead biomass (Mg)",
                                         breaks = breaks_necromass,
                                         labels = labels_necromass)) +
  theme(strip.background = element_blank(),
        strip.text =  element_text(family = "Arial",colour="black", face ="bold", size = 10))

faceted_gaparea_by_biomass

# ggsave("faceted_gaparea_by_biomass.tiff",dpi = 600, width = 6, height = 4,
#        scale = 1.4, compression="lzw")
# ggsave("faceted_gaparea_by_biomass.png",dpi = 600, width = 6, height = 4,
#        scale = 1.4)
getwd()

#####################################################################
#also look at maximum drone area and maximum ground gap area
###the final measurement was the maximum area for all trees
max_ground_area <- regression_covariates_trim %>%
  group_by(strike) %>% arrange(desc(days.post.strike),.by_group = T) %>% slice(1)
max_drone_area <- drone_data %>%
  group_by(strike) %>% arrange(desc(days.post.strike),.by_group = T) %>% slice(1)

#combine the max area datasets
max_area_df <- left_join(max_ground_area,max_drone_area, by = "strike")
str(max_area_df)
nrow(max_area_df);nrow(max_ground_area);nrow(max_drone_area)

#how similar are the area measurements?
mean(max_area_df$cumulative_area);mean(max_area_df$gap_area)
mean(max_area_df$cumulative_area/max_area_df$gap_area)
mean(max_area_df$cumulative_area)/mean(max_area_df$gap_area)#aerial observations are 50% smaller than ground estimates

#look at the per-strike deviation
View(max_area_df[,c("gap_area","cumulative_area")])

max_area_df$gap_area[max_area_df$cumulative_area!=0]
max_area_df$cumulative_area[max_area_df$gap_area=0]
with(max_area_df[max_area_df$gap_area!=0,],mean(cumulative_area/gap_area))

#how similar are the area measurements if we drop recent strikes??
with(max_area_df[max_area_df$survey.days.post.strike>300,],mean(cumulative_area))
with(max_area_df[max_area_df$survey.days.post.strike>300,],mean(gap_area))
with(max_area_df[max_area_df$survey.days.post.strike>300,],
     mean(cumulative_area)/mean(gap_area))
with(max_area_df[max_area_df$survey.days.post.strike>200,],
     mean(cumulative_area)/mean(gap_area))
#the comparisons remain very, very similar

#plot density plots of max area
max_area_df_long <- data.frame("strike" = max_area_df$strike,
                               "Estimate type" = c(rep("Drone",length(max_area_df$cumulative_area)),
                                                   rep("Ground",length(max_area_df$gap_area))),
                               "Gap area" = c(max_area_df$cumulative_area,max_area_df$gap_area))

#for zero gap areas, convert these values to 5m2, which is half the minimum threshold of detection
max_area_df_long$Gap.area_nozero <- max_area_df_long$Gap.area+5 

maxgap_area_comparison_points <- ggplot(max_area_df, aes(x = cumulative_area, y = gap_area)) + 
  annotate("segment",x = 0,y = 0, xend = 800,yend=800, linetype = "dashed")+
  geom_smooth(method = "lm", color = "black") + 
  geom_point(aes(color = centraltree_Dieback)) +
  scale_color_gradient(low = "green1", high = "chocolate4")+
  scale_x_continuous(name = expression(bold("Drone-estimated area"~(m^{2}))),expand = c(0,0),
                     breaks = seq(0,750,250)) +
  scale_y_continuous(name = expression(bold("Ground-estimated area"~(m^{2}))),expand = c(0,0),
                     breaks = seq(0,1000,250)) +
  coord_cartesian(ylim = c(-50,1100), xlim = c(-15,800))+
  theme(legend.position = c(.9,.25),legend.background = element_blank(), legend.title = element_blank()) + 
  theme_basis

maxgap_area_comparison_points

ggsave("maxgap_area_comparison_points.tiff",maxgap_area_comparison_points,
       dpi = 600,height = 2, width = 3.25, scale = 1.8, compression = "lzw")
ggsave("maxgap_area_comparison_points.png",maxgap_area_comparison_points,
       dpi = 600,height = 2, width = 3.25, scale = 1.8)
getwd()

#############################################################################
### --- Now run these models on a log-log scale with final drone data --- ###
#############################################################################
#how many zeros exist?
summary(max_area_df$understory_general_necromass_kg==0)
summary(max_area_df$cumulative_vol==0)
summary(max_area_df$cumulative_area==0)
summary(max_area_df$disturbed_area==0)#this is the area including rooting points of all trees
summary(max_area_df$total.dead==0)

#what did the events with 0 canopy disturbance area do?
with(max_area_df[max_area_df$cumulative_area==0,], mean(total_necromass_kg))/1000
with(max_area_df[max_area_df$cumulative_area==0,], sd(total_necromass_kg))/1000
with(max_area_df[max_area_df$cumulative_area==0,], mean(tree_count))
with(max_area_df[max_area_df$cumulative_area==0,], sd(tree_count))
with(max_area_df[max_area_df$cumulative_area==0,], mean(total.dead))
with(max_area_df[max_area_df$cumulative_area==0,], sd(total.dead))

#add a constant to each variable
max_area_df$cumulative_area_nozero <- max_area_df$cumulative_area+5
max_area_df$cumulative_vol_nozero <- max_area_df$cumulative_vol + 25
max_area_df$understory_general_necromass_kg_nozero <- max_area_df$understory_general_necromass_kg+min(max_area_df$understory_general_necromass_kg[max_area_df$understory_general_necromass_kg!=0])/2
max_area_df$disturbed_area_nozero <- max_area_df$disturbed_area + min(max_area_df$disturbed_area[max_area_df$disturbed_area!=0])/2

#create log variables
max_area_df$log_area <- log(max_area_df$cumulative_area_nozero)
max_area_df$log_volume <- log(max_area_df$cumulative_vol_nozero)
max_area_df$log_necromass <- log(max_area_df$total_necromass_kg)
max_area_df$log_understory_necromass <- log(max_area_df$understory_general_necromass_kg_nozero)
max_area_df$log_overstory_necromass <- log(max_area_df$overstory_necromass_kg)
max_area_df$log_disturbed_area <- log(max_area_df$disturbed_area_nozero)
max_area_df$log_damaged <- log(max_area_df$tree_count)
max_area_df$log_dead <- log(max_area_df$total.dead+1)

#mean height drop seems like it is related to necromass (nothing else really does)
#Necromass
mod_necro_area <- lm(log_necromass ~ log_area, data = max_area_df)
summary(mod_necro_area)#strongly significant
plot(mod_necro_area)#great fit - looks a bit better than non-transformed
mod_necro_vol <- lm(log_necromass ~ log_volume, data = max_area_df)
summary(mod_necro_vol)#strongly significant
plot(mod_necro_vol)#decent fit - looks a bit better than non-transformed

#Overstory necromass
mod_overstorynecro_area <- lm(log_overstory_necromass ~ log_area, data = max_area_df)
summary(mod_overstorynecro_area)#marginally significant
plot(mod_overstorynecro_area)#decent fit - a bit better than non-transformed
mod_overstorynecro_vol <- lm(log_overstory_necromass ~ log_volume, data = max_area_df)
summary(mod_overstorynecro_vol)#barely significant
plot(mod_overstorynecro_vol)#decent fit

#Understory necromass
mod_understorynecro_area <- lm(log_understory_necromass ~ log_area, data = max_area_df)
summary(mod_understorynecro_area)#not significant
plot(mod_understorynecro_area)#good fit
mod_understorynecro_vol <- lm(log_understory_necromass ~ log_volume, data = max_area_df)
summary(mod_understorynecro_vol)#non-significant
plot(mod_understorynecro_vol)#good fit

#Total Disturbed Area
mod_disturb_area <- lm(log_disturbed_area ~ log_area, data = max_area_df)
summary(mod_disturb_area)#weakly significant
plot(mod_disturb_area)#decent fit- better than non-transformed
mod_disturb_vol <- lm(log_disturbed_area ~ log_volume, data = max_area_df)
summary(mod_disturb_vol)#not significant
plot(mod_disturb_vol)#decent fit

#Count of damaged trees
mod_count_area <- lm(log_damaged ~ log_area, data = max_area_df)
summary(mod_count_area)#not significant
plot(mod_count_area)#good fit
mod_count_vol <- lm(log_damaged ~ log_volume, data = max_area_df)
summary(mod_count_vol)#not significant
plot(mod_count_vol)#good fit

#Count of dead trees
mod_dead_area <- lm(log_dead ~ log_area, data = max_area_df)
summary(mod_dead_area)#weakly significant
plot(mod_dead_area)#decent fit
mod_dead_vol <- lm(log_dead ~ log_volume, data = max_area_df)
summary(mod_dead_vol)#weakly significant
plot(mod_dead_vol)#decent fit

# mod_dead_area_pois <- glm(total.dead ~ log_area, data = max_area_df, family="poisson")
# mod_dead_area_pois2 <- glm(total.dead ~ 1, data = max_area_df, family="poisson")
# anova(mod_dead_area_pois,mod_dead_area_pois2,test="LRT")


###################################################################
### -- Plot gap area versus necromass using maximum gap area -- ###
###################################################################

#plot simple graphs of necromass versus gap area and volume
necromass_v_maxgap_simple_loglog <- ggplot(max_area_df, aes(x = cumulative_area_nozero,y = total_necromass_kg)) +
  geom_point() + geom_smooth(method = "lm", color = "black") +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = "Dead biomass (Mg)",breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,9000,1000),seq(10000,100000,10000)), expand = c(.02,0),
                labels = c("0.01",rep("",8),"0.1",rep("",8),"1",rep("",8),"10",rep("",8),"100")) +
  scale_x_log10(name = expression(bold("Canopy gap area"~(m^{2}))),expand = c(0,0),limits=c(4,1250),
                     breaks = c(seq(1,10,1),seq(20,100,10),seq(200,1000,100)),
                                labels=c("1",rep("",8),"10",rep("",8),"100",rep("",8),"1,000"))

necromass_v_maxgap_simple_loglog

# ggsave("necromass_v_maxgap_simple_loglog.tiff",necromass_v_maxgap_simple_loglog,dpi = 600, 
#        scale = 1.8, width = 3.25, height = 2,compression = "lzw")

necromass_v_maxgap_simplevol_loglog <- ggplot(max_area_df, aes(x = cumulative_vol_nozero,y = total_necromass_kg)) +
  geom_point() + geom_smooth(method = "lm", color = "black") +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = "Dead biomass (Mg)",breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,9000,1000),seq(10000,100000,10000)), expand = c(.02,0),
                labels = c("0.01",rep("",8),"0.1",rep("",8),"1",rep("",8),"10",rep("",8),"100")) +
  scale_x_log10(name = expression(bold("Canopy gap volume"~(m^{3}))),expand = c(0.04,0),
                breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,10000,1000)),
                labels=c("10",rep("",8),"100",rep("",8),"1,000",rep("",8),"10,000"))

necromass_v_maxgap_simplevol_loglog

# ggsave("necromass_v_maxgapvol_simple_loglog.tiff",necromass_v_maxgap_simplevol_loglog,dpi = 600, 
#        scale = 1.8, width = 3.25, height = 2,compression = "lzw")


#create a long dataframe separating total, understory, and overstory necromass 
necromass_long <- data.frame("strike" = rep(max_area_df$strike,3),
                             "necromass_type" = c(rep("Total",nrow(max_area_df)),
                                                  rep("Overstory",nrow(max_area_df)),
                                                  rep("Understory",nrow(max_area_df))),
                             "necromass" = c(max_area_df$total_necromass_kg,
                                             max_area_df$overstory_necromass_kg,
                                             max_area_df$understory_general_necromass_kg_nozero),
                             "cumulative_area" = c(max_area_df$cumulative_area_nozero,
                                                   max_area_df$cumulative_area_nozero,
                                                   max_area_df$cumulative_area_nozero),
                             "cumulative_vol" = c(max_area_df$cumulative_vol_nozero,
                                                  max_area_df$cumulative_vol_nozero,
                                                  max_area_df$cumulative_vol_nozero))
#add log-transformed variables
necromass_long$log_necromass <- log(necromass_long$necromass)
necromass_long$log_area <- log(necromass_long$cumulative_area)
necromass_long$log_vol <- log(necromass_long$cumulative_vol)

#reorder the necromass types
necromass_long$necromass_type <- factor(necromass_long$necromass_type,levels = c("Total","Overstory","Understory"))

#plot the data in two figures now for each volume and area
necromass_v_maxgap_loglog <- ggplot(necromass_long, aes(x = cumulative_area,y = necromass, 
                                                   color = necromass_type, fill = necromass_type)) +
  geom_point() + geom_smooth(method = "lm") +
  scale_fill_manual(values = c("black","purple","gold2")) +
  scale_color_manual(values = c("black","purple","gold2")) +
  theme_basis + theme(legend.position = c(.17,.91),legend.title = element_blank())+
  scale_y_log10(name = "Dead biomass (Mg)",breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,9000,1000),seq(10000,100000,10000)), expand = c(.02,0),
                labels = c("0.01",rep("",8),"0.1",rep("",8),"1",rep("",8),"10",rep("",8),"100")) +
  scale_x_log10(name = expression(bold("Canopy disturbance area"~(m^{2}))),expand = c(0,0),limits=c(4,1250),
                breaks = c(seq(1,10,1),seq(20,100,10),seq(200,1000,100)),
                labels=c("1",rep("",8),"10",rep("",8),"100",rep("",8),"1,000"))

necromass_v_maxgap_loglog

ggsave("necromass_v_maxgap_loglog.tiff",necromass_v_maxgap_loglog,dpi = 600, scale = 1.8,
       width = 3.25, height = 2,compression = "lzw")
ggsave("necromass_v_maxgap_loglog.png",necromass_v_maxgap_loglog,dpi = 600, scale = 1.8,
       width = 3.25, height = 2)

#plot these same relationships versus volume
necromass_v_maxgapvol_loglog <- ggplot(necromass_long, aes(x = cumulative_vol,y = necromass, 
                                                      color = necromass_type, fill = necromass_type)) +
  geom_point() + geom_smooth(method = "lm") +
  scale_fill_manual(values = c("black","purple","gold2")) +
  scale_color_manual(values = c("black","purple","gold2")) +
  theme_basis + theme(legend.position = c(.17,.91),legend.title = element_blank())+
  scale_y_log10(name = "Dead biomass (Mg)",breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,9000,1000),seq(10000,100000,10000)), expand = c(.02,0),
                labels = c("0.01",rep("",8),"0.1",rep("",8),"1",rep("",8),"10",rep("",8),"100")) +
  scale_x_log10(name = expression(bold("Canopy disturbance volume"~(m^{3}))),expand = c(0.04,0),
                breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,10000,1000)),
                labels=c("10",rep("",8),"100",rep("",8),"1,000",rep("",8),"10,000"))

necromass_v_maxgapvol_loglog

ggsave("necromass_v_maxgapvol_loglog.tiff",necromass_v_maxgapvol_loglog,dpi = 600, scale = 1.8,
       width = 3.25, height = 2,compression = "lzw")
ggsave("necromass_v_maxgapvol_loglog.png",necromass_v_maxgapvol_loglog,dpi = 600, scale = 1.8,
       width = 3.25, height = 2)


##############################################################################
### -- Create figures demonstrating the insignificant relationships too -- ###
##############################################################################
dmgtrees_v_maxgaparea_loglog <- ggplot(max_area_df, aes(x = cumulative_area_nozero,y = tree_count)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="dashed",se=F) +
  coord_cartesian(ylim = c(.9,120)) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = "Damaged trees",breaks = c(seq(1,10,1),seq(20,100,10)), expand = c(0,0),
                     labels = c("1",rep("",8),"10",rep("",8),"100")) +
  scale_x_log10(name = expression(bold("Canopy gap area"~(m^{2}))),expand = c(0,0),limits=c(4,1250),
                breaks = c(seq(1,10,1),seq(20,100,10),seq(200,1000,100)),
                labels=c("1",rep("",8),"10",rep("",8),"100",rep("",8),"1,000"))

dmgtrees_v_maxgaparea_loglog

# ggsave("dmgtrees_v_maxgaparea_loglog.tiff",dmgtrees_v_maxgaparea_loglog,dpi = 600, 
#        scale = 1.8, width = 3.25, height = 2,compression = "lzw")

dmgtrees_v_maxgapvol_loglog <- ggplot(max_area_df, aes(x = cumulative_vol_nozero,y = tree_count)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="dashed",se=F) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  coord_cartesian(ylim = c(.9,120)) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = "Damaged trees",breaks = c(seq(1,10,1),seq(20,100,10)), expand = c(0,0),
                labels = c("1",rep("",8),"10",rep("",8),"100")) +
  scale_x_log10(name = expression(bold("Canopy gap volume"~(m^{3}))),expand = c(0.04,0),
                breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,10000,1000)),
                labels=c("10",rep("",8),"100",rep("",8),"1,000",rep("",8),"10,000"))

dmgtrees_v_maxgapvol_loglog

# ggsave("dmgtrees_v_maxgapvol_loglog.tiff",dmgtrees_v_maxgapvol_loglog,dpi = 600, 
#        scale = 1.8, width = 3.25, height = 2,compression = "lzw")

deadtrees_v_maxgaparea_loglog <- ggplot(max_area_df, aes(x = cumulative_area_nozero,y = total.dead+1)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="solid",se=T) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = "Dead trees",breaks = c(seq(1,11,1),seq(20,100,10)), expand = c(.02,0),
                labels = c("0",rep("",9),"10",rep("",4),"60","","80","","100"),limits = c(1,60)) +
  scale_x_log10(name = expression(bold("Canopy gap area"~(m^{2}))),expand = c(0,0),limits=c(4,1250),
                breaks = c(seq(1,10,1),seq(20,100,10),seq(200,1000,100)),
                labels=c("1",rep("",8),"10",rep("",8),"100",rep("",8),"1,000"))

deadtrees_v_maxgaparea_loglog

# ggsave("deadtrees_v_maxgaparea_loglog.tiff",deadtrees_v_maxgaparea_loglog,dpi = 600, 
#        scale = 1.8, width = 3.25, height = 2,compression = "lzw")

deadtrees_v_maxgapvol_loglog <- ggplot(max_area_df, aes(x = cumulative_vol_nozero,y = total.dead+1)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="solid",se=T) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = "Dead trees",breaks = c(seq(1,11,1),seq(20,100,10)), expand = c(.02,0),
                labels = c("0",rep("",9),"10",rep("",4),"60","","80","","100"),limits = c(1,60)) +
  scale_x_log10(name = expression(bold("Canopy gap volume"~(m^{3}))),expand = c(0.04,0),
                breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,10000,1000)),
                labels=c("10",rep("",8),"100",rep("",8),"1,000",rep("",8),"10,000"))

deadtrees_v_maxgapvol_loglog

# ggsave("deadtrees_v_maxgapvol_loglog.tiff",deadtrees_v_maxgapvol_loglog,dpi = 600, 
#        scale = 1.8, width = 3.25, height = 2,compression = "lzw")

disturbedarea_v_maxgapvol <- ggplot(max_area_df, aes(x = cumulative_vol_nozero,y = disturbed_area_nozero)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="dashed",se=F) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = expression(bold("Disturbed area"~(m^{2}))),expand = c(0.02,0),
                breaks = c(seq(10,100,10),seq(200,1000,100),2000),
                labels = c("10",rep("",8),"100",rep("",8),"1,000","")) +
  scale_x_log10(name = expression(bold("Canopy gap volume"~(m^{3}))),expand = c(0.04,0),
                breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,10000,1000)),
                labels=c("10",rep("",8),"100",rep("",8),"1,000",rep("",8),"10,000"))

disturbedarea_v_maxgapvol

# ggsave("disturbedarea_v_maxgapvol.tiff",disturbedarea_v_maxgapvol,dpi = 600, 
#        scale = 1.8, width = 3.25, height = 2,compression = "lzw")

disturbedarea_v_maxgaparea <- ggplot(max_area_df, aes(x = cumulative_area_nozero,y = disturbed_area_nozero)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="solid",se=T) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  # coord_cartesian(ylim = c(0,120),xlim=c(0,11000)) +
  scale_y_log10(name = expression(bold("Disturbed area"~(m^{2}))),expand = c(0.02,0),
                breaks = c(seq(10,100,10),seq(200,1000,100),2000),
                labels = c("10",rep("",8),"100",rep("",8),"1,000","")) +
  scale_x_log10(name = expression(bold("Canopy gap area"~(m^{2}))),expand = c(0,0),limits=c(4,1250),
                breaks = c(seq(1,10,1),seq(20,100,10),seq(200,1000,100)),
                labels=c("1",rep("",8),"10",rep("",8),"100",rep("",8),"1,000"))

disturbedarea_v_maxgaparea

# ggsave("disturbedarea_v_maxgaparea.tiff",disturbedarea_v_maxgaparea,dpi = 600, 
#        scale = 1.8, width = 3.25, height = 2,compression = "lzw")

######################################################################
### -- Make figures corresponding to create multi-panel figures -- ###
######################################################################

#figure order: left = area; right = volume; top = dmg; mid = dead; bottom = area
dmgtrees_v_maxgaparea_comb <- ggplot(max_area_df, aes(x = cumulative_area_nozero,y = tree_count)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="dashed",se=F) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = "Damaged trees",breaks = c(seq(1,10,1),seq(20,100,10)), expand = c(0.02,0),
                labels = c("1",rep("",8),"10",rep("",8),"100")) +
  scale_x_log10(name = element_blank(),expand = c(0,0),limits=c(4,1250),
                breaks = c(seq(1,10,1),seq(20,100,10),seq(200,1000,100)),
                labels=c("1",rep("",8),"10",rep("",8),"100",rep("",8),"1,000"))

dmgtrees_v_maxgaparea_comb

dmgtrees_v_maxgapvol_comb <- ggplot(max_area_df, aes(x = cumulative_vol_nozero,y = tree_count)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="dashed",se=F) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  # coord_cartesian(ylim = c(0,120),xlim=c(0,11000)) +
  scale_y_log10(name = element_blank(),breaks = c(seq(1,10,1),seq(20,100,10)), expand = c(0.02,0),
                labels = c("1",rep("",8),"10",rep("",8),"100")) +
  scale_x_log10(name = element_blank(),expand = c(0.04,0),
                breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,10000,1000)),
                labels=c("10",rep("",8),"100",rep("",8),"1,000",rep("",8),"10,000"))

dmgtrees_v_maxgapvol_comb

deadtrees_v_maxgaparea_comb <- ggplot(max_area_df, aes(x = cumulative_area_nozero,y = total.dead+1)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="solid",se=T) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = "Dead trees",breaks = c(seq(1,11,1),seq(20,100,10)), expand = c(.02,0),
                labels = c("0","1",rep("",8),"10",rep("",4),"60","","80","","100"),limits = c(1,60)) +
  scale_x_log10(name = element_blank(),expand = c(0,0),limits=c(4,1250),
                breaks = c(seq(1,10,1),seq(20,100,10),seq(200,1000,100)),
                labels=c("1",rep("",8),"10",rep("",8),"100",rep("",8),"1,000"))

deadtrees_v_maxgaparea_comb

deadtrees_v_maxgapvol_comb <- ggplot(max_area_df, aes(x = cumulative_vol_nozero,y = total.dead+1)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="solid",se=T) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = element_blank(),breaks = c(seq(1,11,1),seq(20,100,10)), expand = c(.02,0),
                labels = c("0","1",rep("",8),"10",rep("",4),"60","","80","","100"),limits = c(1,60)) +
  scale_x_log10(name = element_blank(),expand = c(0.04,0),
                breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,10000,1000)),
                labels=c("10",rep("",8),"100",rep("",8),"1,000",rep("",8),"10,000"))

deadtrees_v_maxgapvol_comb

disturbedarea_v_maxgapvol_comb <- ggplot(max_area_df, aes(x = cumulative_vol_nozero,y = disturbed_area_nozero)) +
  geom_point() + geom_smooth(method = "lm", color = "black",linetype="dashed",se=F) +
  theme_basis + theme(legend.position = c(.15,.85),legend.title = element_blank())+
  scale_y_log10(name = element_blank(),expand = c(0.02,0),
                breaks = c(seq(10,100,10),seq(200,1000,100),2000),
                labels = c("10",rep("",8),"100",rep("",8),"1,000","")) +
  scale_x_log10(name = expression(bold("Canopy gap volume"~(m^{3}))),expand = c(0.04,0),
                breaks = c(seq(10,90,10),seq(100,900,100),seq(1000,10000,1000)),
                labels=c("10",rep("",8),"100",rep("",8),"1,000",rep("",8),"10,000"))

disturbedarea_v_maxgapvol_comb

disturbedarea_v_maxgaparea#this remains unchanged

#########################################
### -- Create an aggregated figure -- ###
#########################################
library(egg)
library(gridExtra)

comb_fig <- ggarrange(dmgtrees_v_maxgaparea_comb,dmgtrees_v_maxgapvol_comb,
                      deadtrees_v_maxgaparea_comb,deadtrees_v_maxgapvol_comb,
                      disturbedarea_v_maxgaparea,disturbedarea_v_maxgapvol_comb,
                      labels = c("a","b","c","d","e","f"))

# ggsave("comb_fig.tiff",comb_fig,width = 6.5,height = 5,dpi = 600,
#        scale=1.45,compression="lzw")
# ggsave("comb_fig.png",comb_fig,width = 6.5,height = 5,dpi = 600,
#        scale=1.45)



