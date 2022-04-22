add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');

# Checkout https://tex.stackexchange.com/a/44316
sub run_makeglossaries {
    my ($base_name, $path) = fileparse( $_[0] ); #handle -outdir param by splitting path and file, ...
    pushd $path; # ... cd-ing into folder first, then running makeglossaries ...

    if ( $silent ) {
        system "makeglossaries -q '$base_name'";
    }
    else {
        system "makeglossaries '$base_name'";
    };

    popd; # ... and cd-ing back again
}

add_cus_dep("nlo", "nls", 0, "nlo2nls");
sub nlo2nls {
    system("makeindex $_[0].nlo -s nomencl.ist -o $_[0].nls -t $_[0].nlg");
}
