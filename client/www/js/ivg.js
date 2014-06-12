var ivg = {

    setBaseUrl: function(aBaseUrl)
    {
        this.baseUrl = aBaseUrl;
    },

    fillUserList: function(tagId)
    {
        $.ajax({
            url: this.baseUrl + '/users',
            type: 'GET',
            dataType: 'json',
            error : function () {
                ivg.showServerError();
            },
            success: function (data) {
                list = "";
                for(i = 0; i < data["users"].length; i++)
                {
                    list += '<div data-role="collapsible" id="' + data["users"][i]["nickname"] + '"><h3>' + data["users"][i]["fullname"] + '</h3>';
                    list += '<p><div id="' + data["users"][i]["nickname"] + '-points">';
                    list += '</div>';
                    list += '<a id="' + data["users"][i]["nickname"] + '-btn" ';
                    list += 'href="javascript:ivg.addPoint(\'' + data["users"][i]["nickname"] + '\', 120)" ';
                    list += 'class="ui-btn">Bock hinzuf&uuml;gen</a></p>';
                    list += '</div>';
                }
                $(tagId).html(list).collapsibleset('refresh');

                for(i = 0; i < data["users"].length; i++)
                {
                    $('#' + data["users"][i]["nickname"]).collapsible({
                        expand: function(event, ui) { ivg.updateUser(event.target.id); },
                    });
                }
            }
        });
    },

    updateUser: function(nickname)
    {
        $.mobile.loading("show");
        $('#' + nickname + '-btn').addClass('ui-disabled');

        $.ajax({
            url: this.baseUrl + '/users/' + nickname,
            type: 'GET',
            dataType: 'json',
            error : function () {
                $.mobile.loading("hide");
                $('#' + nickname + '-btn').removeClass('ui-disabled');
                ivg.showServerError();
            },
            success: function (data) {
                list = "";
                for(i = 0; i < data["user"]["points"].length; i++)
                {
                    list += '<img src="./img/goat' + i + '.png"/>';
                }
                $('#' + nickname + '-points').html(list);
                $.mobile.loading("hide");
                $('#' + nickname + '-btn').removeClass('ui-disabled');
            }
        });
    },

    addPoint: function(nickname, weight)
    {
         $.mobile.loading("show");
         $('#' + nickname + '-btn').addClass('ui-disabled');

         $.ajax({
            url: this.baseUrl + '/points',
            type: 'POST',
            data: { 'nickname': nickname, 'weight': weight },
            error : function (xhr, status, text) {
              $.mobile.loading("hide");
              $('#' + nickname + '-btn').removeClass('ui-disabled');
              if(xhr.status == 460)
              {
                ivg.showMaxPointsError();
              }
              else if(xhr.status == 461)
              {
                ivg.showOffTimePointsError();
              }
              else
              {
                ivg.showServerError();
              }
            },
            success: function (data) {
                $.mobile.loading("hide");
                $('#' + nickname + '-btn').removeClass('ui-disabled');
                ivg.updateUser(nickname);
            }
        });
    },

    showServerError: function()
    {
        $.mobile.changePage('#serverError', {
            transition: 'pop',
            changeHash: true,
            role: 'dialog'
        });
    },

    showMaxPointsError: function()
    {
        $("#maxPointsError").popup("open");
    },

    showOffTimePointsError: function()
    {
        $("#offTimePointsError").popup("open");
    },
};