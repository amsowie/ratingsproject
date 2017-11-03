"use strict";

$(document).ready(function() {

  $("#score").on('keyup', function() {
    let ratingInput = $("#score").val();
    ratingInput = Number(ratingInput);
    if (( isNaN(ratingInput) ) || ( ratingInput < 1 ) || ( ratingInput > 5 )) {
      $("#rating_num_text").html("Digit 1 to 5, please.");
      $("#submit_rating").attr("disabled", true);
    } else {  
      $("#rating_num_text").html("");
      $("#submit_rating").removeAttr("disabled");

    } // end if
  } //end func score eval
  );

  $("#form_rate_movie").on('submit', function(evt) {
    evt.preventDefault();

    let formInputs = {
      "user_id": $('#user_id').val(),
      "movie_id": $('#movie_id').val(),
      "score": $('#score').val()
    };

    $.post('/movies/rating', formInputs, function(results) {
      $('#urating').text('You rated this movie a ' + results.message);
      $('#score').val('');
    } // end func(results)
    );

  } // end sendRating
  );

} // end func doc.ready
);