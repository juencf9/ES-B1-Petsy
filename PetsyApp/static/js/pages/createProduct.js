$(document).ready(function () {
    $("#input-fa").fileinput({
        theme: "fa",
        uploadUrl: "/file-upload-batch/2",
        allowedFileExtensions: ["jpg", "png", "gif"]
    });
});