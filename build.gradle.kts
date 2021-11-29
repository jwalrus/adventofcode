plugins {
    kotlin("jvm") version "1.4.10"
    kotlin("kapt") version "1.4.20"
}

group = "jwalrus"
version = "1.0-SNAPSHOT"

val arrowVersion = "0.11.0"
val kotestVersion = "4.3.1"

repositories {
    jcenter()
    mavenCentral()
}

dependencies {
    kapt("io.arrow-kt:arrow-meta:$arrowVersion")
    implementation(kotlin("stdlib-jdk8"))
    implementation("io.arrow-kt:arrow-core:$arrowVersion")
    implementation("io.arrow-kt:arrow-fx:$arrowVersion")
    implementation("io.arrow-kt:arrow-syntax:$arrowVersion")
    testImplementation("io.kotest:kotest-runner-junit5:$kotestVersion")
    testImplementation("io.kotest:kotest-assertions-core:$kotestVersion")
    testImplementation("io.kotest:kotest-property:$kotestVersion")
}

tasks {
    compileKotlin {
        kotlinOptions.jvmTarget = "1.8"
        kotlinOptions.freeCompilerArgs = listOf("-Xinline-classes", "-nowarn")
    }
    compileTestKotlin {
        kotlinOptions.jvmTarget = "1.8"
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}