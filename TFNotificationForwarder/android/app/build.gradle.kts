plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.skillfusion.tfnotificationforwarder"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.skillfusion.tfnotificationforwarder"
        minSdk = 26
        targetSdk = 35
        versionCode = 20000
        versionName = "2.0.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }
}

dependencies {
}
