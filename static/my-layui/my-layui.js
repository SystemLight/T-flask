var myLayuiFormPool = {};
var myLayuiDialogPool = {};
var myLayuiFormDialogPool = {};

const MyLayuiForm = (function () {
    const cls = function (formID, receipt, autoRender) {
        this.formID = formID;
        this.receipt = receipt;
        this._formValue = {};

        if (autoRender) {
            var self = this;
            $(function () {
                self.render();
            });
        }
    };

    cls.prototype = {
        render() {
            var self = this;

            layui.form.render(null, this.formID);

            // render file
            $('form[lay-filter=' + this.formID + ']').children('[mylayui-skin="file"]').each(function () {
                var name = $(this).attr('mylayui-name');
                var mockInput = $('<input class="layui-input layui-disabled" type="text" disabled>');
                var chooseFileButton = $('<button type="button" class="layui-btn">选择文件</button>');
                var fileInput = $('<input type="file" name="' + name + '" class="layui-hide">');
                var formItem = $(this);

                formItem.append(fileInput);
                formItem.children('.layui-input-block.pure__d-flex').append(mockInput).append(chooseFileButton);

                chooseFileButton.on('click', function () {
                    fileInput.click();
                });

                fileInput.on('change', function (e) {
                    var val = $(this).val();
                    mockInput.val(val.substring(val.lastIndexOf('\\') + 1));
                    self._formValue[name + '[files]'] = $(this)[0].files[0];
                });
            });
        },
        getData: function () {
            return $.extend({}, this._formValue, layui.form.val(this.formID))
        },
        getFormData: function (receipt) {
            var jsonVal = this.getJsonData(receipt);
            var fd = new FormData();
            $.each(jsonVal, function (key, value) {
                fd.append(key, value);
            });
            return fd;
        },
        getJsonData: function (receipt) {
            if (!receipt) {
                receipt = this.receipt;
            }

            var resultData = {};
            var cacheData = this.getData();
            var self = this;
            $.each(receipt, function (index, value) {
                if (value[0] === 'CheckBox') {
                    resultData[value[1][0]] = self['get' + value[0] + 'Val'](cacheData, value[1][0], value[1][2].map(function (v) {
                        return v[0];
                    }));
                    return;
                }
                if (self['get' + value[0] + 'Val']) {
                    resultData[value[1][0]] = self['get' + value[0] + 'Val'](cacheData, value[1][0])
                }
            });
            return resultData;
        },
        getTextInputVal: function (data, name) {
            return data[name];
        },
        getFileInputVal: function (data, name) {
            return data[name + '[files]'];
        },
        getNumberInputVal: function (data, name) {
            return Number(data[name]);
        },
        getPasswordInputVal: function (data, name) {
            return data[name];
        },
        getSelectVal: function (data, name) {
            return data[name];
        },
        getCheckBoxVal: function (data, name, options) {
            var result = []
            $.each(options, function (index, option) {
                if (data[name + '[' + option + ']'] === 'on') {
                    result.push(option);
                }
            })
            return result;
        },
        getSwitchVal: function (data, name) {
            return Boolean(data[name]);
        },
        getRadioBoxVal: function (data, name) {
            return data[name];
        },
        getTextareaVal: function (data, name) {
            return data[name];
        }
    };

    return cls;
})();

const MyLayuiDialog = (function () {
    const cls = function (dialogID) {
        this.dialogID = dialogID;
        this._index = null;
    };

    cls.prototype = {
        open: function (option) {
            this._index = layui.layer.open($.extend({
                type: 1,
                move: false,
                area: ['auto', '320px'],
                content: $('#layui-dialog-' + this.dialogID + '-template').text()
            }, option));
        },
        close: function () {
            layui.layer.close(this._index);
        }
    };

    return cls;
})();

const MyLayuiFormDialog = (function () {
    const cls = function (dialog, form) {
        this.dialog = dialog;
        this.form = form;
    };

    cls.prototype = {
        open: function (title, end) {
            var self = this;
            this.dialog.open({
                title: title,
                success: function () {
                    self.form.render();
                },
                end: end
            });
        },
        close: function () {
            this.dialog.close();
        }
    };

    return cls;
})();
