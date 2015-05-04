jQuery(function($) {
  // Switch these values out for your specific contact email address
  var address_name = "address_name"
  var domain = "gmail.com"
    // Add email via js to prevent scrapers getting at it. This will be displayed if the form breaks
  var full = address_name + "@" + domain

  $("#contact_form").submit(function() {
    var email = $("#e_field").val(); // get email field value
    var name = $("#n_field").val(); // get name field value
    var msg = $("#m_field").val(); // get message field value
    var isValid = true

    var errMsg = ''
    if (name == undefined) {
      errMsg += "Please enter a valid Name \n"
    }

    if (msg == undefined) {
      errMsg += "Please enter a valid Message \n"
    }

    // Super simple email check. Does it look like a duck?
    if (email == undefined || !/(.+)@(.+){2,}\.(.+){2,}/.test(email)) {
      errMsg += "Please enter a valid Email \n"
    }

    if (errMsg.length > 1) {
      alert(errMsg)
      return false
    }

    $("#contact_form").html("<img class='busy-loading' src='/images/ajax-loader.gif' />")

    $.ajax({
        type: "POST",
        url: "/c/contact_me",
        data: JSON.stringify({
          'message': {
            'from_email': email,
            'from_name': name,
            'headers': {
              'Reply-To': email
            },
            'subject': 'sammar.co contact submission',
            'text': msg
          }
        }),
        contentType: "application/json"
      })
      .done(function(response) {
        // Hide the form... Add the thank you ;)
        $("#contact_form").fadeOut('slow', function() {
          $(this).html("<h2>Thank you ;)</h2>")
        }).fadeIn("slow");

      })
      .fail(function(response) {
        $("#contact_form").fadeOut('slow', function() {
          $(this).html("<h2>Whooops! An error sending that email. Please email me at <a href='mailto:" + full + "'>" + full + "</a></h2>")
        }).fadeIn("slow");
      });
    return false; // prevent page refresh
  });
});