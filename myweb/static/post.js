// dealing with upload image and post new psot

function uploadImage(image) {
    var formdata = new FormData();
    formdata.append("image", image);

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
            // console.log(url);
            path=url;
        },
        error: function(data) {
            console.log(data);
        }
    });
    return path;
};


function post_form(type,path){
            
    content= $('#summernote').summernote('code');
    var title=$('#title').val();
    console.log(title)

    const form = document.createElement('form');
    form.method = 'post';
    form.action = path;

    const hiddeninput = document.createElement('input');
    hiddeninput.name='type';
    hiddeninput.type='hidden';
    hiddeninput.value=type;
    form.appendChild(hiddeninput);

    const hiddentitle = document.createElement('input');
    hiddentitle.name='title';
    hiddentitle.type='hidden';
    hiddentitle.value=title;
    form.appendChild(hiddentitle);

    const hiddenField = document.createElement('textarea');
    hiddenField.name='content';
    hiddenField.style="display:none;";
    hiddenField.value=content;
    form.appendChild(hiddenField);

    document.body.appendChild(form);
    form.submit();

};