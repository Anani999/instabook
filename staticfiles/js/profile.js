// Get the modal
var modal = document.getElementById("upload-modal");

// Get the button that opens the modal
var btn = document.getElementById("open-upload-modal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

const fileInput = document.getElementById('file');

const contentTypeRadios = document.getElementsByName('content_type');

contentTypeRadios.forEach(radio => {
  radio.addEventListener('change', (event) => {
    const selectedType = event.target.value;
    if (selectedType === 'image') {
      fileInput.accept = 'image/*';
    } else if (selectedType === 'video') {
      fileInput.accept = 'video/*';
    }
  });
});


function commentPost(postId,csrfToken) {
  // Send AJAX request to comment on a post
  $.ajax({
      type: "POST",
      url: "/comment-post/",
      data: {
          post_id: postId,
          comment: $('#new-comment-' + postId).val(),
          csrfmiddlewaretoken: csrfToken
      },
      success: function(data) {
          // Update comment count in the UI
          $('#comment-count-' + postId).text(data.comments);
          // Clear comment input field
          $('#new-comment-' + postId).val('');
      }
  });
}

function likePost(postId,csrfToken){
  $.ajax({
    type:'POST',
    url:'/like-post/',
    data:{
      post_id:postId,
      csrfmeddlewaretoken:csrfToken
    },success:function(data){
      $('#likes-count-'+postId).text(data.likes)
      console.log(data);
    }
  });
}

function sharePost(postId,csrfToken){
  $.ajax({
    type:'POST',
    url:'/share-post/',
    data:{
      post_id:postId,
      csrfmeddlewaretoken:csrfToken,
    },success:function(data){
      $('#share-count-'+postId).text(data.shares);
    }
  })
}


function showPost(currentIndex) {
  const postViews = document.getElementsByClassName('.post-view');

  // Handle potential errors (e.g., no posts or invalid index)
  if (!postViews || currentIndex < 0 || currentIndex >= postViews.length) {
    return;
  }

  for (let i = 0; i < postViews.length; i++) {
    postViews[i].style.display = i === currentIndex ? 'block' : 'none';
  }
}

function handleRightArrowClick() {
  const currentPostIndex = parseInt(document.getElementById('current-post-index').textContent, 10);
  const nextIndex = currentPostIndex + 1;
  showPost(nextIndex);
  document.getElementById('current-post-index').textContent = nextIndex;
}

function handleLeftArrowClick() {
  const currentPostIndex = parseInt(document.getElementById('current-post-index').textContent, 10);
  const previousIndex = Math.max(currentPostIndex - 1, 0); // Ensure index doesn't go below 0
  showPost(previousIndex);
  document.getElementById('current-post-index').textContent = previousIndex;
}

// Initial call to show the first post
showPost(0); // Assuming posts are indexed starting from 0
