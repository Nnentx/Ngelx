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

android {
    namespace = "com.nnentx.ngelx_app"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "com.nnentx.ngelx_app"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = 26
        targetSdk = flutter.targetSdkVersion
        // Uses the version code from pubspec.yaml. When using split APKs, 1000 * ABI_VERSION
        // is added automatically by Flutter. (https://developer.android.com/studio/build/configure-apk-splits#configure-APK-versions)
        // You can force using the value of versionCode by specifying the `-P force-version-code-ignoring-abi=true`
        // flag during build.
        versionCode = flutter.versionCode
        versionName = flutter.versionName
        ndk {
            abiFilters += listOf("armeabi-v7a", "arm64-v8a")
        }
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
                // CI test APK'ları aynı anahtarla imzalansın; rastgele runner
                // debug anahtarı paket güncellemelerini bozmasın.
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
                // CI debug APK'lari da acikca kalici test anahtariyla imzalansin.
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

val bnbSdkVersion = rootProject.extra["bnb_sdk_version"] as String

dependencies {
    implementation("com.banuba.sdk:face_tracker:$bnbSdkVersion")
    implementation("com.banuba.sdk:background:$bnbSdkVersion")
    implementation("com.banuba.sdk:lips:$bnbSdkVersion")
    implementation("com.banuba.sdk:skin:$bnbSdkVersion")
}

val copyBanubaEffects by tasks.registering(Copy::class) {
    from(file("../../effects"))
    into(file("src/main/assets/bnb-resources/effects"))
}

tasks.named("preBuild") {
    dependsOn(copyBanubaEffects)
}

flutter {
    source = "../.."
}
