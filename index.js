// document.getElementById('task_text').addEventListener('keydown', function handleKeyDown(event) {
//     if (event.key === 'Enter" && !event.shiftKey) {
//         event.preventDefault(); // Prevent the default Enter key behavior
//         var txt = document.getElementById('task_text');
//         if (txt.value === ''){
//             return;
//         }
//         var lists = document.getElementsByClassName('tasks')[0];
//         var list_ = document.createElement('li');
//         var alink = document.createElement('a');
//         var txt = document.createElement('div');
//         txt.innerText = document.getElementById('task_text').value;
//         var div = document.createElement('div');
//         div.className = 'options';
//         var btn = document.createElement('button');
//         btn.className = 'options edit';
//         var img = document.createElement('img');
//         img.src = 'assets/edit.png';
//         img.width = 20;
//         img.height = 20;
//         btn.appendChild(img);
//         var btn2 = document.createElement('button');
//         btn2.className = 'options delete';
//         var img2 = document.createElement('img');
//         img2.src = 'assets/delete.png';
//         img2.width = 20;
//         img2.height = 20;
//         btn.appendChild(img2);
//         div.appendChild(btn);
//         div.appendChild(btn2);
//         alink.appendChild(txt);
//         list_.appendChild(alink)
//         list_.appendChild(div);
//         lists.appendChild(list_)
//         document.getElementById('task_text').value = '';
//     }
// })

// document.getElementById('addlist_btn').addEventListener('click', function (e) {
//     e.preventDefault();
//     var input_list = document.createElement('input');
//     var add_btn = document.getElementById('addlist_btn');
//     var parent = document.getElementsByClassName('bottom-leftpane')[0];
//     input_list.id = 'input_list';
//     input_list.className = 'addlist';
//     input_list.type = 'text';
//     input_list.autocomplete = 'off';
//     input_list.maxLength = 20;
//     parent.appendChild(input_list);
//     add_btn.style.display = 'none';
//     input_list.focus();

//     document.getElementById('input_list').addEventListener('blur', function () {
//         parent.appendChild(add_btn);
//         parent.removeChild(input_list);
//         add_btn.style.display = 'block';
//     });

//     document.getElementById('input_list').addEventListener('keyup', function handleKeyDown(event) {
//         if (event.key === "Enter" && !event.shiftKey) {
//             event.preventDefault(); // Prevent the default Enter key behavior
//             if (input_list.value === ''){
//                 return;
//             }
//             var lists = document.getElementsByClassName('lists')[0];
//             var list_ = document.createElement('li');
//             var alink = document.createElement('a');
//             var txt = document.createElement('span');
//             txt.innerText = document.getElementById('input_list').value;
//             var div = document.createElement('div');
//             div.className = 'options';
//             var btn = document.createElement('button');
//             btn.className = 'options edit';
//             var img = document.createElement('img');
//             img.src = 'assets/edit.png';
//             img.width = 20;
//             img.height = 20;
//             btn.appendChild(img);
//             var btn2 = document.createElement('button');
//             btn2.className = 'options delete';
//             var img2 = document.createElement('img');
//             img2.src = 'assets/delete.png';
//             img2.width = 20;
//             img2.height = 20;
//             btn.appendChild(img2);
//             div.appendChild(btn);
//             div.appendChild(btn2);
//             alink.appendChild(txt);
//             list_.appendChild(alink)
//             list_.appendChild(div);
//             lists.appendChild(list_)

//             input_list.value = '';
//         }
//     })
// });



$(document).ready(function () {
    $("#task_text").on({
        input: function () {
            $(this).height(0); // Reset the height to 0
            $(this).height(this.scrollHeight);
        },
        keypress: function () {
            $(this).css({
                borderBottom: '1.5px solid saddlebrown'
            }, 500).show(200);
        }
    });
});




$(document).delegate('.task_delete','click', function () {
    var me = $(this);
    $(me).parents('li').animate({
        width: 0,
        height: 0,
        opacity: 0
    }, 400, function () {
        $(me).parents('li').remove();
    })
})

$(document).delegate(
    '.task_edit',
    'click', function () {
        var span = $(this).parents('li').children('span');
        var input = $('<textarea id="editarea" autocomplete="off" maxlength=200 class="taskedit" rows=5 >').val(span.text());
        input.css({
            height: span.height(),
            width: span.width()
        })
        span.replaceWith(input);
        $('#editarea').on('input', function () {
            $(this).height(0); // Reset the height to 0
            $(this).height(this.scrollHeight);
            submit.prop('disabled', false);
            if ($(this).val().trim() === "") {
                submit.prop('disabled', true);
            }
        }
        )
        var submit = $('<button type="submit" class="tasksubmit">Submit</button>');
        var cancel = $('<button type="submit" class="cancelsubmit">Cancel</button>');
        var li = $(this).parents('li');
        var editoptions = $('<div class="editoptions"></div>').append(submit,cancel);
        li.append(editoptions);
        li.css('flex-direction', 'column');
        li.children('div .options').hide();
        submit.prop('disabled',true);
        $(document).delegate(
            '.cancelsubmit', 'click', function () {
                li.css('flex-direction', 'row');
                li.children('div .editoptions').hide();
                li.children('div .options').show(500);
                span.show();
                input.hide();
            }
        )
        $(document).delegate('.tasksubmit', 'click', function (e) {
            li.css('flex-direction', 'row');
            li.children('div .editoptions').hide();
            li.children('div .options').show(500);
            var s = $('<span>').text(input.val());
            input.replaceWith(s);
            input.css({
                height: 0,
                width: 0
            })
        })
    })



document.getElementById('task_text').addEventListener('keypress', function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        addTask();
    }
});

function addTask() {
    var textarea_ = $("#task_text");
    if (textarea_.val().trim() == "") {
        return false;
    }
    let userInput = textarea_.val();
    console.log(userInput)
    let item = $('<li>').append($('<span>').text(userInput));
    item.hide().appendTo('.tasks').fadeOut(500, function () {
        $(this).fadeIn(500, function () {
        });
    });
    // item.
    $(".tasks").append(item);
    $(".tasks li").last().append("<div class='options'><button class = 'task_edit' ><img src='assets/edit.svg' alt='edit svg'></button><button class='task_delete' ><img src='assets/delete.svg' alt='delete svg'></button></div>")
    textarea_.val('');
    textarea_.height('');
    var myElement = $('.tasks');
    myElement.scrollTop((myElement[0].scrollHeight + 100) - myElement.outerHeight());
    
};

function addList() {
    var parent = $('#addlist_btn').parent();
    var child = $('#addlist_btn');
    parent.children().replaceWith($('<input id="input_list" class="addlist" type="text" autocomplete="off" maxlength="20" placeholder="Name your list">'));
    parent.children().focus();

    $('.addlist').on({
        keydown: function (e) {
            var myElement = $('.lists');
            if (e.key === 'Enter') {
                if ($('.addlist').val().trim() == '') {
                    return;
                }
                let userInput = $('.addlist').val();
                let item = $('<li>').append($('<a>').append($('<span>').text(userInput))).hide(300).show(300, function(){
                    myElement.scrollTop((myElement[0].scrollHeight) - myElement.outerHeight())
                });
                $('.lists').append(item);
                $(".lists li").last().append("<div><button class = 'list_task_edit' ><img src='assets/edit.svg' alt='edit svg'></button><button class='task_delete'><img src='assets/delete.svg' alt='delete svg'></button></div>")
                
                parent.animate({
                    opacity: 0
                }, 200, function () {
                    parent.children().replaceWith(child)
                }).animate({
                    opacity: 1
                }, 200, function () {
                    parent.children().replaceWith(child)
                })
            }
        },
        blur: function () {
            $(this).animate({
                width: 0,
                opacity: 0
            }, 300,
                function () {
                    parent.animate({
                        opacity: 1
                    }, 400, function () {
                        parent.children().replaceWith(child)
                    })
                });
        },
    }
    )
}

