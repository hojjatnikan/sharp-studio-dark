// Gradle build for the plugin marketplace route.
//
// The plugin is pure resources (a UI theme descriptor plus an icon pack), so it
// needs no compilation at all. `python tools/build_plugin.py` packages exactly
// the same JAR/ZIP without any download; use this Gradle build when you want the
// IntelliJ Platform tooling (verifier, signing, publishing to the marketplace).
//
//   ./gradlew buildPlugin        -> build/distributions/*.zip
//   ./gradlew verifyPlugin        (needs the JetBrains marketplace verifier)
//   ./gradlew runIde             -> start Rider with the plugin installed

plugins {
    id("java")
    id("org.jetbrains.intellij.platform") version "2.5.0"
}

group = "com.hnikan.rider"
version = "1.0.0"

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        // Rider 2026.2 (build 262). Swap the type for IntelliJPlatformType.IntellijIdeaCommunity
        // if you only want to compile against the core platform.
        rider("2026.2")
        testFramework(org.jetbrains.intellij.platform.gradle.TestFrameworkType.Platform)
    }
}

intellijPlatform {
    pluginConfiguration {
        ideaVersion {
            sinceBuild = "251"
            // no untilBuild: open-ended compatibility (and the marketplace validator
            // rejects guessed build numbers)
        }
    }
}

tasks {
    // The plugin only ships resources, and the IDE distribution is not needed to
    // assemble them; both tasks are skippable but harmless if left enabled.
    buildSearchableOptions {
        enabled = false
    }
    patchPluginXml {
        sinceBuild.set("251")
        // untilBuild intentionally unset -- see the note above
    }
    withType<JavaCompile> {
        sourceCompatibility = "21"
        targetCompatibility = "21"
    }
}
