var editor = new EditorJS({
    readOnly: false,

    holder: 'editorjs',

    tools: {
      header: {
        class: Header,
        inlineToolbar: ['marker', 'link'],
        config: {
          placeholder: 'Header'
        },
        shortcut: 'CMD+SHIFT+H'
      },
       image: {
          class: ImageTool,
          config: {
            endpoints: {
              byFile: 'http://localhost:8008/uploadFile', // Your backend file uploader endpoint
              byUrl: 'http://localhost:8008/fetchUrl', // Your endpoint that provides uploading by Url
            }
          }
      },

      list: {
        class: List,
        inlineToolbar: true,
        shortcut: 'CMD+SHIFT+L'
      },

      checklist: {
        class: Checklist,
        inlineToolbar: true,
      },

      quote: {
        class: Quote,
        inlineToolbar: true,
        config: {
          quotePlaceholder: 'Enter a quote',
          captionPlaceholder: 'Quote\'s author',
        },
        shortcut: 'CMD+SHIFT+O'
      },

      warning: Warning,

      marker: {
        class:  Marker,
        shortcut: 'CMD+SHIFT+M'
      },

      code: {
        class:  CodeTool,
        shortcut: 'CMD+SHIFT+C'
      },

      delimiter: Delimiter,

      inlineCode: {
        class: InlineCode,
        shortcut: 'CMD+SHIFT+C'
      },

      linkTool: LinkTool,

      embed: Embed,

      table: {
        class: Table,
        inlineToolbar: true,
        shortcut: 'CMD+ALT+T'
      },

    },

    
    onReady: function(){
      console.log('Editor.js is ready to work!')
      
    },
    onChange: function(api, event) {
      console.log('something changed', event);
    }
  });

  const postButton = document.getElementById('btnpost');
  const draftButton = document.getElementById('btndraft');

  // postButton.addEventListener('click',post_to_url('/test','post'));
  postButton.addEventListener('click', ()=>{
    editor.save()
      .then((savedData) => {
          post_form('/post/new','post',savedData)
          console.log('data saved')
      })
      .catch((error) => {
        console.error('Saving error', error);
      });
  },false);


  function post_form(path,type,data){
      const form = document.createElement('form');
      form.method = 'post';
      form.action = path;
      data['type']=type;

      const hiddenField = document.createElement('textarea');
      hiddenField.name='data'
      hiddenField.value=JSON.stringify(data)
      form.appendChild(hiddenField)

      document.body.appendChild(form);
      form.submit();

  };