{ pkgs }: {
    deps = [
        pkgs.python39Packages.django
        pkgs.python39Full
        pkgs.python39Packages.pillow
        pkgs.python39Packages.django-crispy-forms
        pkgs.python39Packages.django-extensions
        pkgs.python39Packages.pygraphviz
    ];
}