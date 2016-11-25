/**
 * Created by vphrase on 22/11/16.
 */


$( document ).on( "mousemove", function( event ) {
    if (event.pageX <25) {
        $("#wrapper").removeClass('toggled');
    }
    if (event.pageX >200){
        $("#wrapper").addClass('toggled');
    }
});
