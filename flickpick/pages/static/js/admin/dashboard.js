/*********************************************************************
 *  Global scope
 **********************************************************************/
flickpick.dashboard = flickpick.dashboard || {};


django.jQuery(function ($) {
    /*********************************************************************
     *  cached DOM elements
     **********************************************************************/

    flickpick.dashboard.collapsible             = $( ".module_title.grp-collapse-handler:parent" );

    /*********************************************************************
     *  functions
     **********************************************************************/


    /*********************************************************************
     * Page Ready
     **********************************************************************/

    $(document).ready(function () {
        var collapseState = flickpick.cookieJar.getCookie("dashboard_state");
        if (!collapseState)
            collapseState = {};
        if ( collapseState == {} ) {
            flickpick.dashboard.collapsible.each(function() {
                collapseState[this.id] = $( this ).hasClass('grp-open');
            });
            flickpick.cookieJar.setCookie("dashboard_state", collapseState);
        }else {
            $.each(collapseState, function(key, value) {
                var myDiv = $("#"+key);
                if (!value) {
                    myDiv.toggleClass('grp-open').toggleClass('grp-closed');
                }
            });
        }

        $(document).on('click', flickpick.dashboard.collapsible, function(event){
            var my_parent = $( event.target).parent();
            var my_id = my_parent.attr('id');
            var has_class = my_parent.hasClass('grp-open');
            collapseState[my_id] = has_class ? true : false;
            flickpick.cookieJar.setCookie("dashboard_state", collapseState);
        });

    })
});