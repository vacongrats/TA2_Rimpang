function tampilkanPreview(gambar, idpreview) {
  //                membuat objek gambar
  var gb = gambar.files;
  //                loop untuk merender gambar
  for (var i = 0; i < gb.length; i++) {
    //                    bikin variabel
    var gbPreview = gb[i];
    var imageType = /image.*/;
    var preview = document.getElementById(idpreview);
    var reader = new FileReader();
    if (gbPreview.type.match(imageType)) {
      //                        jika tipe data sesuai
      preview.file = gbPreview;
      reader.onload = (function (element) {
        return function (e) {
          element.src = e.target.result;
        };
      })(preview);
      //                    membaca data URL gambar
      reader.readAsDataURL(gbPreview);
    } else {
      //                        jika tipe data tidak sesuai
      alert("Type file tidak sesuai. Khusus image.");
    }
  }
}

console.log("ok");

$(document).ready(function () {
  $('#dtBasicExample').DataTable();
  $('.dataTables_length').addClass('bs-select');
});
