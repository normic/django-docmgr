function ImageRefresher() {
};

function init(inputId) {
    var that = this;
    this.inputId = '#' + inputId;
    this.imgId = '#' + inputId + '_img';
    this.origData = $(this.imgId).attr('src');
    $(this.inputId).change(function(){
        that.readURL(this);
    });
}

function readURL(input) {
    var that = this;
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $(that.imgId).attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    } else {
        $(this.imgId).attr('src', this.origData);
    }
}

ImageRefresher.prototype.init = init;
ImageRefresher.prototype.readURL = readURL;

// check if jQuery is loaded at all
if (!window.jQuery) {
    console.log('Warn: jQuery is missing, trying to load it myself.')
    var jq = document.createElement('script'); jq.type = 'text/javascript';
    jq.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'
    document.getElementsByTagName('head')[0].appendChild(jq);

    window.onload = function() {
        $('.document-preview').each(function(index) {
            var refresher = new ImageRefresher();
            refresher.init(this.id);
        });
    };
}
