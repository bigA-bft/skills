

# 引入SDK

```java
/******************** Project build.gradle ********************/
buildscript {
    repositories {
        maven {
            url "https://artifact.bytedance.com/repository/pangle"  //穿山甲融合SDK依赖
        }
	}
}
allprojects {
    repositories {
        maven {
            url "https://artifact.bytedance.com/repository/pangle"  //穿山甲融合SDK依赖
        }
	}
}
```

```java
/******************** App build.gradle ********************/
depedencies {
	//注：adn如果通过aar方式引入，需要把对应的adn aar放到libs目录下，注意aar名称和版本号需要和下面命令行匹配上
	implementation fileTree(include: ['*.jar'], dir: 'libs')
	implementation 'com.pangle.cn:mediation-sdk:7.6.1.1' //穿山甲融合SDK

}

```

## 初始化对接

```java
//初始化聚合sdk
private void initMediationAdSdk(Context context) {
    TTAdSdk.init(context, buildConfig(context));
    TTAdSdk.start(new TTAdSdk.Callback() {
        @Override
        public void success() {
            //初始化成功
            //在初始化成功回调之后进行广告加载
        }

        @Override
        public void fail(int i, String s) {
            //初始化失败
        }
    });
}

// 构造TTAdConfig
private TTAdConfig buildConfig(Context context) {
	return new TTAdConfig.Builder()
			.appId("5823835") //APP ID
			.appName("ix cam") //APP Name
			.useMediation(true)  //开启聚合功能
			.debug(true)  //打开debug开关
			.themeStatus(0)  //正常模式  0是正常模式；1是夜间模式；
			/**
            * 多进程增加注释说明：V>=5.1.6.0支持多进程，如需开启可在初始化时设置.supportMultiProcess(true) ，默认false；
            * 注意：开启多进程开关时需要将ADN的多进程也开启，否则广告展示异常，影响收益。
            * CSJ、gdt无需额外设置，KS、baidu、Sigmob、Mintegral需要在清单文件中配置各家ADN激励全屏xxxActivity属性android:multiprocess="true"
            */
            .supportMultiProcess(false)  //不支持
			.customController(getTTCustomController())  //设置隐私权
			.build();
}
//设置隐私合规
private TTCustomController getTTCustomController() {
	return new TTCustomController() {
		@Override
		public boolean isCanUseLocation() {  //是否授权位置权限
			return true;
		}

		@Override
		public boolean isCanUsePhoneState() {  //是否授权手机信息权限
			return true;
		}

		@Override
		public boolean isCanUseWifiState() {  //是否授权wifi state权限
			return true;
		}

		@Override
		public boolean isCanUseWriteExternal() {  //是否授权写外部存储权限
			return true;
		}

		@Override
		public boolean isCanUseAndroidId() {  //是否授权Android Id权限
			return true;
		}

		@Override
		public MediationPrivacyConfig getMediationPrivacyConfig() {
			return new MediationPrivacyConfig() {
				@Override
				public boolean isLimitPersonalAds() {  //是否限制个性化广告
					return false;
				}

				@Override
				public boolean isProgrammaticRecommend() {  //是否开启程序化广告推荐
					return true;
				}
			};
		}
	};
}

```

### 接入开屏广告

```java

//构造开屏广告的Adslot
private AdSlot buildSplashAdslot() {
    return new AdSlot.Builder()
            .setCodeId("123*****") //广告位ID
			.build();
}


// 加载开屏广告
private void loadSplashAd(Activity act) {
    TTAdNative adNativeLoader = TTAdSdk.getAdManager().createAdNative(act);
    adNativeLoader.loadSplashAd(buildSplashAdslot(), new TTAdNative.CSJSplashAdListener() {
        @Override
        public void onSplashLoadSuccess() {
            //广告加载成功
        }

        @Override
        public void onSplashLoadFail(CSJAdError csjAdError) {
            //广告加载失败
        }

        @Override
        public void onSplashRenderSuccess(CSJSplashAd csjSplashAd) {
            //广告渲染成功，在此展示广告
            showSplashAd(csjSplashAd, splashContainer); //注 ：splashContainer为展示Banner广告的容器
        }

        @Override
        public void onSplashRenderFail(CSJSplashAd csjSplashAd, CSJAdError csjAdError) {
            //广告渲染失败
        }
    }, 3500);
}


//展示开屏广告
private void showSplashAd(CSJSplashAd splashAd, FrameLayout container) {
    if (splashAd == null || container == null) {
        return;
    }

    splashAd.setSplashAdListener(new CSJSplashAd.SplashAdListener() {
        @Override
        public void onSplashAdShow(CSJSplashAd csjSplashAd) {
            //广告展示
            //获取展示广告相关信息，需要再show回调之后进行获取
            MediationBaseManager manager = splashAd.getMediationManager();
            if (manager != null && manager.getShowEcpm() != null) {
                MediationAdEcpmInfo showEcpm = manager.getShowEcpm();
                String ecpm = showEcpm.getEcpm(); //展示广告的价格
                String sdkName = showEcpm.getSdkName();  //展示广告的adn名称
                String slotId = showEcpm.getSlotId(); //展示广告的代码位ID
            }
        }

        @Override
        public void onSplashAdClick(CSJSplashAd csjSplashAd) {
            //广告点击
        }

        @Override
        public void onSplashAdClose(CSJSplashAd csjSplashAd, int i) {
            //广告关闭
        }
    });
    splashAd.showSplashView(container);//展示开屏广告
}

```

### 接入信息流广告

```java

//构造信息流Adslot
private AdSlot buildNativeAdslot() {
    return new AdSlot.Builder()
            .setCodeId("123*****") //广告位ID
			/**
            * 注：
            *  1:单位为px
            *  2:如果是信息流自渲染广告，设置广告图片期望的图片宽高 ，不能为0
            *  2:如果是信息流模板广告，宽度设置为希望的宽度，高度设置为0(0为高度选择自适应参数)
            */
            .setImageAcceptedSize(320, 0)
			.setAdCount(1)//请求广告数量为1到3条 （优先采用平台配置的数量）
			.setMediationAdSlot(// 聚合广告请求配置
            new MediationAdSlot.Builder()
                    .setMuted(true)
                    .build())
			.build();
}



//加载信息流广告
private void loadNativeAd(Activity act) {
    TTAdNative adNativeLoader = TTAdSdk.getAdManager().createAdNative(act);
    adNativeLoader.loadFeedAd(buildNativeAdslot(), new TTAdNative.FeedAdListener() {
        private TTFeedAd mTTFeedAd;
        @Override
        public void onError(int erroCode, String errorMsg) {
            //广告加载失败
        }

        @Override
        public void onFeedAdLoad(List<TTFeedAd> list) {
            //广告加载成功
            //信息流广告渲染具体参考demo
            //如果是自渲染下载类广告可以通过以下api获取下载六要素
            if (list != null && list.size() > 0) {
                mTTFeedAd = list.get(0);
                ComplianceInfo complianceInfo = mTTFeedAd.getComplianceInfo();
                if (complianceInfo != null){
                    String appName = complianceInfo.getAppName(); //应用名称
                    String appVersion = complianceInfo.getAppVersion(); //应用版本号
                    String developerName = complianceInfo.getDeveloperName(); //开发者名称
                    String privacyUrl = complianceInfo.getPrivacyUrl(); //隐私协议Url
                    Map<String, String> permissionsMap = complianceInfo.getPermissionsMap(); //权限名称及权限描述列表
                    String permissionUrl = complianceInfo.getPermissionUrl(); //权限列表url
                    String functionDescUrl = complianceInfo.getFunctionDescUrl(); //应用功能url
                } else {
                    //非下载类广告
                }
            }
        }

        @Override
        public void onRenderSuccess(View view, float v, float v1, boolean b) {
            if (mTTFeedAd != null) {
                View expressFeedView = mTTFeedAd.getAdView();
                // ...
            }
        }
    });
}

```

### 接入激励广告

```java
//构造激励视频广告的Adlsot
private AdSlot buildRewardAdlost(){
	return new AdSlot.Builder()
			.setCodeId("123*****")  //广告位ID
			.setOrientation(TTAdConstant.VERTICAL)  //激励视频方向
			.setMediationAdSlot(
				new MediationAdSlot.Builder()
					.setMuted(true)
					.setRewardName("领取积分")
					.setRewardAmount(1)
					.build()
			)
			.build();
}


//加载激励视频
private void loadRewardAd(Activity act) {
    TTAdNative adNativeLoader = TTAdSdk.getAdManager().createAdNative(act);
    /** 这里为激励视频的简单功能，如需使用复杂功能，如gromore的服务端奖励验证，请参考demo中的AdUtils.kt类中激励部分 */
    adNativeLoader.loadRewardVideoAd(buildRewardAdlost(), new TTAdNative.RewardVideoAdListener() {
        @Override
        public void onError(int errorCode, String errorMsg) {
            //广告加载失败
        }

        @Override
        public void onRewardVideoAdLoad(TTRewardVideoAd ttRewardVideoAd) {
            //广告加载成功
        }

        @Override
        public void onRewardVideoCached() {
            //广告缓存成功 此api已经废弃，请使用onRewardVideoCached(TTRewardVideoAd ttRewardVideoAd)
        }

        @Override
        public void onRewardVideoCached(TTRewardVideoAd ttRewardVideoAd) {
            //广告缓存成功 在此回调中进行广告展示
            showRewardAd(act, ttRewardVideoAd);
        }
    });
}

//展示激励视频
private void showRewardAd(Activity act, TTRewardVideoAd ttRewardVideoAd) {
    if (act == null || ttRewardVideoAd == null) {
        return;
    }

    ttRewardVideoAd.setRewardAdInteractionListener(new TTRewardVideoAd.RewardAdInteractionListener() {
        @Override
        public void onAdShow() {
            //广告展示
            //获取展示广告相关信息，需要再show回调之后进行获取
            MediationBaseManager manager = ttRewardVideoAd.getMediationManager();
            if (manager != null && manager.getShowEcpm() != null) {
                MediationAdEcpmInfo showEcpm = manager.getShowEcpm();
                String ecpm = showEcpm.getEcpm(); //展示广告的价格
                String sdkName = showEcpm.getSdkName();  //展示广告的adn名称
                String slotId = showEcpm.getSlotId(); //展示广告的代码位ID
            }
        }

        @Override
        public void onAdVideoBarClick() {
            //广告点击
        }

        @Override
        public void onAdClose() {
            //广告关闭
        }

        @Override
        public void onVideoComplete() {
            //广告视频播放完成
        }

        @Override
        public void onVideoError() {
            //广告视频错误
        }

        @Override
        public void onRewardVerify(boolean rewardVerify, int rewardAmount, String rewardName, int errorCode, String errorMsg) {
            //奖励发放 已废弃 请使用 onRewardArrived 替代
        }

        @Override
        public void onRewardArrived(boolean isRewardValid, int rewardType, Bundle extraInfo) {
            //奖励发放
            if (isRewardValid) {
                // 验证通过
                // 从extraInfo读取奖励信息
            } else {
                // 未验证通过
            }
        }

        @Override
        public void onSkippedVideo() {
            //广告跳过
        }
    });
    ttRewardVideoAd.showRewardVideoAd(act); //展示激励视频
}


```


