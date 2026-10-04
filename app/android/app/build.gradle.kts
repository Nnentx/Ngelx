import java.util.Properties

plugins {
    id("com.android.application")
    id("com.google.gms.google-services")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystorePropertiesFile.inputStream().use { keystoreProperties.load(it) }
}

// Paket 2 and Paket 3 use Firebase's registered Paket 1 test application ID
// so google-services can configure installable side-test APKs.
val ngelxP2SideBySide =
    (project.findProperty("ngelxP2SideBySide") as String?)?.toBoolean() ?: false
val ngelxP3SideBySide =
    (project.findProperty("ngelxP3SideBySide") as String?)?.toBoolean() ?: false
val ngelxSideBySide = ngelxP2SideBySide || ngelxP3SideBySide

android {
    namespace = "com.nnentx.ngelx_app"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    defaultConfig {
        applicationId = if (ngelxSideBySide) {
            "com.nnentx.ngelx_app.p1test"
        } else {
            "com.nnentx.ngelx_app"
        }
        manifestPlaceholders["appLabel"] =
            when {
                ngelxP3SideBySide -> "NgelX P3 Test"
                ngelxP2SideBySide -> "NgelX P2 Test"
                else -> "NgelX"
            }

        minSdk = 23
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    signingConfigs {
        if (keystorePropertiesFile.exists()) {
            create("ngelxRelease") {
                keyAlias = keystoreProperties["keyAlias"] as String
                keyPassword = keystoreProperties["keyPassword"] as String
                storeFile = file(keystoreProperties["storeFile"] as String)
                storePassword = keystoreProperties["storePassword"] as String
            }
        } else {
            create("ngelxStableTest") {
                keyAlias = "androiddebugkey"
                keyPassword = "android"
                storeFile = file("${System.getProperty("user.home")}/.android/debug.keystore")
                storePassword = "android"
            }
        }
    }

    buildTypes {
        debug {
            if (!keystorePropertiesFile.exists()) {
                signingConfig = signingConfigs.getByName("ngelxStableTest")
            }
        }
        release {
            signingConfig = if (keystorePropertiesFile.exists()) {
                signingConfigs.getByName("ngelxRelease")
            } else {
                signingConfigs.getByName("ngelxStableTest")
            }
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}
