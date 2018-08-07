$(document)
  .ready(function() {

    // fix menu when passed
    $('.masthead')
      .visibility({
        once: false,
        onBottomPassed: function() {
          $('.fixed.menu').transition('fade in');
        },
        onBottomPassedReverse: function() {
          $('.fixed.menu').transition('fade out');
        }
      })
    ;

    // create sidebar and attach to menu open
    $('.ui.sidebar')
      .sidebar('attach events', '.toc.item')
    ;

    var path = window.location.pathname.split('/').pop();

    if (path == '') {
      path = '/backoffice';

      if ($('.glide__1').length) {
        var glide1 = new Glide('.glide__1', {
          type: 'slider',
          autoplay: 5000,
          hoverPause: true,
        }).mount();
      }

      if ($('.glide__2').length) {
        var glide2 = new Glide('.glide__2', {
          type: 'slider',
          autoplay: 5000,
          hoverPause: true,
        }).mount();
      }
    }

    else if (path == 'my_post') {
      path = '/backoffice/' + path;
    }

    var target = $('div a.item[href="'+ path +'"]');

    target.addClass('active');

    $('.ui.dropdown').dropdown();

    $('#newPost').click(function () {
      $('.ui.tiny.modal').modal('show');
    });

    $('.linkable').click(function () {
      window.location = $(this).attr('data-href');
    });

    $('.commentForm').submit(function (e) {
      e.preventDefault();
      create_comment($(this), path);
    });

    function create_comment(element, path) {
      element.children('button').addClass('loading');
      $.ajax({
        url : '/backoffice/post/comment/' + path,
        type : "POST",
        data : {
          'comment' : element.find('#id_comment').val()
        },
        dataType: 'json',

        success : function (data) {
          element.find('#id_comment').val('');
          avatar = JSON.parse(data.avatar[0])
          user = JSON.parse(data.user)
          if (avatar[0].fields.avatar == '') {
            avatar[0].fields.avatar = 'avatar/hacker.png';
          }
          element.before(
            `
            <div class="comment">
              <a class="avatar">
                <img src="/static/backoffice/images/${avatar[0].fields.avatar}">
              </a>
              <div class="content">
                <a class="author">${user[0].fields.first_name} ${user[0].fields.last_name}</a>
                <div class="metadata">
                  <span class="date">${data.date_comment}</span>
                </div>
                <div class="text">${data.comment}</div>
                <div class="actions">
                  <a class="delete" href="post/comment/delete/${data.id_comment}">Delete</a>
                </div>
              </div>
            </div>
            `
          );
          increaseValue($('.commentCount'));
          element.children('button').removeClass('loading');
          // location.reload();
        },
        error : function (e) {
          console.log('error');
          console.log(e);
          element.children('button').removeClass('loading');
        }
      });
    };

    $('#like').click(function () {
      add_likes($(this), path);
    });

    function add_likes(element, path) {
      $.ajax({
        url: '/backoffice/post/like/' + path,
        dataType: 'json',
      }).done(function(result) {
        increaseValue($('.likeCount'));
      })
    }

    function increaseValue(element) {
      commentCount = parseInt(element.text());
      element.text(commentCount + 1);
    }

    function deacreaseValue(element) {
      commentCount = parseInt(element.text());
      element.text(commentCount - 1);
    }

    $('.delete').click(function (e) {
      remove_post(e, $(this));
    });

    function remove_post(event, element) {
      event.preventDefault();
      $.ajax({
        url: element.attr('href'),
        dataType: 'json'
      }).done(function(result) {
        element.parents('.comment').remove();
        deacreaseValue($('.commentCount'));
      })
    }

    $('[data-fancybox]').fancybox({
      buttons: [
        "fullScreen",
        "download",
        "close"
      ]
    });

});
