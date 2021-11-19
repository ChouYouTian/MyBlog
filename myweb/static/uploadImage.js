function uploadImage(image) {

    console.log(image['name'])
    var formdata = new FormData();
    formdata.append("image", image,image['name']);

    var path;
    $.ajax({
      url: '/saveimg',
      cache: false,
      contentType: false,
      processData: false,
      async : false,
      data: formdata,
      type: "post",
      success: function(url) {
        console.log(url);
        path=url;
      },
      error: function(data) {
          console.log(data);
      }
    });
    return path;
};