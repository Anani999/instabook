

function openBelow(){
    const items = document.getElementById('dropdown-content');

    if (items.style.display == 'block'){
        items.style.display = 'none'
    }else{
        items.style.display = 'block'
    }
  }

    function likePost(postId,csrfToken) {
        // Send AJAX request to like a post
        $.ajax({
            type: "POST",
            url: "/like-post/",
            data: {
                post_id: postId,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(data) {
                // Update like count in the UI
                $('#like-count-' + postId).text(data.likes);
            }
        });
    }

    function commentPost(postId) {
        // Send AJAX request to comment on a post
        $.ajax({
            type: "POST",
            url: "/comment-post/",
            data: {
                post_id: postId,
                comment: $('#comment-text-' + postId).val(),
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(data) {
                // Update comment count in the UI
                $('#comment-count-' + postId).text(data.comments);
                // Clear comment input field
                $('#comment-text-' + postId).val('');
            }
        });
    }

    function sharePost(postId) {
        // Send AJAX request to share a post
        $.ajax({
            type: "POST",
            url: "/share-post/",
            data: {
                post_id: postId,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(data) {
                // Update share count in the UI
                $('#share-count-' + postId).text(data.shares);
            }
        });
    }
