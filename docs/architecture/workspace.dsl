workspace "speclint" "Minimal C1/C2 for speclint — sole source for container views." {

    model {
        user = person "User" "Runs the CLI."
        system = softwareSystem "speclint" "Stdlib-only spec linter." {
            api = container "CLI" "Command-line tool" "Python" "Lints spec.md structural rules."
        }
        user -> system "Uses"
    }

    views {
        systemContext system "SystemContext" {
            include *
            autoLayout
        }
        container system "Containers" {
            include *
            autoLayout
        }
    }
}
