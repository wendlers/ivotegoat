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
            error : function (){ document.title='error'; },
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
                    list += 'class="ui-btn">Add Gote</a></p>';
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
        $.ajax({
            url: this.baseUrl + '/users/' + nickname,
            type: 'GET',
            dataType: 'json',
            error : function (){ document.title='error'; },
            success: function (data) {
                list = "";
                for(i = 0; i < data["user"]["points"].length; i++)
                {
                    list += '<img src="./img/goat.png"/>';
                }
                $('#' + nickname + '-points').html(list);
            }
        });
    },

    addPoint: function(nickname, weight)
    {
        $.ajax({
            url: this.baseUrl + '/points',
            type: 'POST',
            data: { 'nickname': nickname, 'weight': weight },
            error : function (){ document.title='error'; },
            success: function (data) {
                ivg.updateUser(nickname);
            }
        });
    },
};