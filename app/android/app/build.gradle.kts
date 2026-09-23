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

val ngelxBrandResDir = layout.buildDirectory.dir("generated/ngelxBrandRes").get().asFile
val prepareNgelxBrandResources = tasks.register<Copy>("prepareNgelxBrandResources") {
    from(rootProject.file("../assets/ngelx_logo.png"))
    into(file("${ngelxBrandResDir}/drawable-nodpi"))
    rename { "ngelx_launcher_mark.png" }
}

android {
    namespace = "com.nnentx.ngelx_app"
    sourceSets.getByName("main").res.srcDir(ngelxBrandResDir)
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
        minSdk = 23
        targetSdk = flutter.targetSdkVersion
        // Uses the version code from pubspec.yaml. When using split APKs, 1000 * ABI_VERSION
        // is added automatically by Flutter. (https://developer.android.com/studio/build/configure-apk-splits#configure-APK-versions)
        // You can force using the value of versionCode by specifying the `-P force-version-code-ignoring-abi=true`
        // flag during build.
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

tasks.configureEach {
    if (name.startsWith("merge") && name.endsWith("Resources")) {
        dependsOn(prepareNgelxBrandResources)
    }
}

flutter {
    source = "../.."
}
