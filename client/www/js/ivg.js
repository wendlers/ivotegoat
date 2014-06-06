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

                    for(j = 0; j < data["users"][i]["points"].length; j++)
                    {
                        list += '<img src="./img/goat.png"/>';
                    }

                    list += '</div>';
                    list += '<a href="javascript:ivg.addPoint(\'' + data["users"][i]["nickname"] + '\', 60)" ';
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

        $.ajax({
            url: this.baseUrl + '/users/' + nickname,
            type: 'GET',
            dataType: 'json',
            error : function () {
                $.mobile.loading("hide");
                ivg.showServerError();
            },
            success: function (data) {
                list = "";
                for(i = 0; i < data["user"]["points"].length; i++)
                {
                    list += '<img src="./img/goat.png"/>';
                }
                $('#' + nickname + '-points').html(list);
                $.mobile.loading("hide");
            }
        });
    },

    addPoint: function(nickname, weight)
    {
         $.ajax({
            url: this.baseUrl + '/points',
            type: 'POST',
            data: { 'nickname': nickname, 'weight': weight },
            error : function (xhr, status, text) {
              if(xhr.status == 400)
              {
                ivg.showMaxPointsError();
              }
              else
              {
                ivg.showServerError();
              }
            },
            success: function (data) {
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
        $.mobile.changePage('#maxPointsError', {
            transition: 'pop',
            changeHash: true,
            role: 'dialog'
        });
    },
};