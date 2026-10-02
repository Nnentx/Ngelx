extra["bnb_sdk_version"] = "1.18.+"

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

val newBuildDir: Directory =
    rootProject.layout.buildDirectory
        .dir("../../build")
        .get()
rootProject.layout.buildDirectory.value(newBuildDir)

subprojects {
    val newSubprojectBuildDir: Directory = newBuildDir.dir(project.name)
    project.layout.buildDirectory.value(newSubprojectBuildDir)
}
subprojects {
    project.evaluationDependsOn(":app")
}

tasks.register<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}


/*
 * banuba_sdk Flutter plugin'i upstream olarak compileSdkVersion 31 ile geliyor.
 * NgelX'in güncel AndroidX bağımlılıkları API 34+ istiyor.
 * Tüm alt projeler değerlendirildikten sonra Banuba library compileSdk'ini 36'ya
 * yükseltiyoruz; böylece plugin'in kendi build.gradle dosyasındaki 31 değeri
 * sonradan geri yazılamıyor.
 */
gradle.projectsEvaluated {
    val banuba = project(":banuba_sdk")
    val androidExtension = banuba.extensions.findByName("android")
    val compileSdkMethod = androidExtension?.javaClass?.methods?.firstOrNull {
        it.name == "compileSdkVersion" &&
            it.parameterCount == 1 &&
            (it.parameterTypes[0] == Int::class.javaPrimitiveType ||
                it.parameterTypes[0] == Int::class.javaObjectType)
    }
    requireNotNull(compileSdkMethod) {
        "banuba_sdk Android compileSdk override method bulunamadi."
    }
    compileSdkMethod.invoke(androidExtension, 36)
}
