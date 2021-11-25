let doValidate = (el) => {
    const $this = $(el);
    let result = validateEmail($this.val().toLowerCase())
    setInputBehaviour($this, result);
    result
    ? $("#btnSend").attr("disabled", false)
    : $("#btnSend").attr("disabled", true);
    };

let validateEmail = (val) => {
	return /^(([a-z0-9!#$%&'*+/=?^_`{|}~-]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
		val
	);
};

let setInputBehaviour = ($this, val) => {
	val ? $this.removeClass("is-danger") : $this.addClass("is-danger");
	return val;
};