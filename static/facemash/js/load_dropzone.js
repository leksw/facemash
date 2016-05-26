"use strict";

$ = $ || django.jQuery;

var maxImageWidth = 2800,
    maxImageHeight = 2800;

$(document).ready(function(){

    //Dropzone.autoDiscover = false;
    Dropzone.options.uploadDropzone = {
   
        // Make sure only images are accepted
        acceptedFiles: "image/*",
        addRemoveLinks: true,
        autoProcessQueue: false,
        uploadMultiple: true,
        parallelUploads: 20,

        init: function() {
            var uploadDropzone = this,
            submitButton = $('#button-upload');

            // Register for the thumbnail callback.
            // When the thumbnail is created the image dimensions are set.
            this.on("thumbnail", function(file) {
              // Do the dimension checks you want to do
              if (file.width > maxImageWidth || file.height > maxImageHeight) {
                file.rejectDimensions();
              }
              else {
                file.acceptDimensions();
              }
            });

            this.on("complete", function(file) {
                this.removeFile(file);
            });

            this.on("success", function(file, responseText) {
                if (!!document.homeRequest) {
                    location.reload(); 
                    homeRequest.loadRequest();
                }
                console.log(responseText.success);
            });
            
            this.on("sendingmultiple", function(file, xhr, formData) {
                // Will send the filesize along with the file as POST data.
                formData.append("quantity", file.length);
            });

            submitButton.on('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                uploadDropzone.processQueue();
            });
            
            $('#loadModal').on('hidden.bs.modal', function () {
                 uploadDropzone.removeAllFiles();
            });
        },
      
        // Instead of directly accepting / rejecting the file, setup two
        // functions on the file that can be called later to accept / reject
        // the file.
        accept: function(file, done) {
          file.acceptDimensions = done;
          file.rejectDimensions = function() { done("Invalid dimension."); };
          // Of course you could also just put the `done` function in the file
          // and call it either with or without error in the `thumbnail` event
          // callback, but I think that this is cleaner.
        }
    };
    
});
