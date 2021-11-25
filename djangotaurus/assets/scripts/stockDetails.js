let maxBuyable;
let lotQtyValid = [false];
let sellBuyValid = [false];
let sellSellValid = [false];
$(document).ready(() => {
    candleChart(chart_date, chart_data);
    maxBuyable = getMaxAmtBuyable();
    $("input[type='number']").keydown(function (e) { 
        if (this.value.length > maxBuyable.toString().length) {
            this.value = this.value.slice(0,maxBuyable.toString().length); 
        }
    });
});
let doValidate = (el) => {
	let $this = $(el);
	switch ($this.attr("id")) {
		case "purAmount":
            try{
                lotQtyValid[0] = validateQty($this.val());
				setInputBehaviour($this, lotQtyValid[0]);
				break;
            }
            catch(e){
                lotQtyValid[0]=false;
                break
            }
        case "iptSellBuyOption":
            try{
                sellBuyValid[0] = validateOwned($this.val(),$this.data("owned"));
				setInputBehaviour($this, sellBuyValid[0]);
				break;
            }
            catch(e){
                sellBuyValid[0]=false;
                break
            }
        case "iptSellSellOption":
            try{
                sellSellValid[0] = validateOwned($this.val(),$this.data("owned"));
                setInputBehaviour($this, sellSellValid[0]);
                break;
            }
            catch(e){
                sellSellValid[0]=false;
                break;
            }				
	}
    switch ($this.attr("id")) {
		case "purAmount":
            let qtyResult = lotQtyValid.every((e) => e === true);
            qtyResult
                ? $("#btnConfirmBuy").attr("disabled", false)
                : $("#btnConfirmBuy").attr("disabled", true);
            break;
        case "iptSellBuyOption":
            let sbResult = sellBuyValid.every((e) => e === true);
            sbResult
                ? $("#btnSellBuyOption").attr("disabled", false)
                : $("#btnSellBuyOption").attr("disabled", true);
            break;
        case "iptSellSellOption":
            let ssResult = sellSellValid.every((e) => e === true);
            ssResult
                ? $("#btnSellSellOption").attr("disabled", false)
                : $("#btnSellSellOption").attr("disabled", true);
            break;	
	}
};
let getMaxAmtBuyable=()=>{
    const current_price = $("#cPrice").data("cprice");
    const balance = $("#balance").data("balance");
    let limit = balance/current_price;
    return Number.parseInt(limit);
}
let validateDigit=(val)=>{
    return /^\d+$/.test(val);
}
let validateQty=(val)=>{
    if (validateDigit(val) && val <= maxBuyable){
        return true;
    }
    return false;
}
let validateOwned=(val,owned)=>{
	if (validateDigit(val) && (owned >=val) && (val != 0)){
        return true;
    }
    return false;
}

let setInputBehaviour = ($this, val) => {
	val ? $this.removeClass("is-danger") : $this.addClass("is-danger");
    if ($this.attr("id") == "purAmount"){
        val ? $("#purAmountError").addClass("is-hidden") : $("#purAmountError").removeClass("is-hidden");
    }
    if ($this.attr("id") == "iptSellBuyOption"){
        val ? $("#iptSellBuyOptionError").addClass("is-hidden") : $("#iptSellBuyOptionError").removeClass("is-hidden");
    }
    if ($this.attr("id") == "iptSellSellOption"){
        val ? $("#iptSellSellOptionError").addClass("is-hidden") : $("#iptSellSellOptionError").removeClass("is-hidden");
    }
	return val;
};
$("#purAmount").keyup((e)=> { 
    try{
        let cprice = parseFloat($("#cPrice").text().substring(1));
        let qty = $(e.target).val();
        let total = cprice*qty
        $("#ttlPrice").val("SGD "+total.toFixed(3));
    }
    catch(e){}; 
});
$("#iptSellBuyOption").keyup((e)=> {
    try{
        let price = parseFloat($(e.target).data("price"));
        let qty = $(e.target).val();
        let total = price*qty
        $("#totalForSB").text("Sell for SGD "+total.toFixed(3));
    }
    catch(e){}; 
});
$("#iptSellSellOption").keyup((e)=> { 
    try{
        let price = parseFloat($(e.target).data("price"));
        let qty = $(e.target).val();
        let total = price*qty
        $("#totalForSS").text("Sell for SGD "+total.toFixed(3));
    }
    catch(e){}; 
});
let setTab = (el) =>{
    const $this = $(el);
    if ($this.hasClass('is-active')){
        return 0;
    }
    else{
        let prev = $this.parent().children('.is-active');
        let prevContent = $(prev).data("target");
        $(prev).removeClass("is-active");
        $(prevContent).addClass("is-hidden");

        $this.addClass("is-active");
        let target = $this.data("target");
        $(target).removeClass("is-hidden");
    }
}

$("#btnPStock").click(() => {
    $("html").addClass("is-clipped");
    $("#modal-purc").addClass("is-active");
});

$("#btnSStock").click(() => {
    $("html").addClass("is-clipped");
    $("#modal-sell").addClass("is-active");
});

$(".delete").click(() => {
    $("html").removeClass("is-clipped");
    $("#modal-sell").removeClass("is-active");
    $("#modal-purc").removeClass("is-active");
});

$("#btnCancelBuy").click(() => {
    $("html").removeClass("is-clipped");
    $("#modal-sell").removeClass("is-active");
    $("#modal-purc").removeClass("is-active");
});
$("#btnCancelSell").click(() => {
    $("html").removeClass("is-clipped");
    $("#modal-sell").removeClass("is-active");
    $("#modal-purc").removeClass("is-active");
});

$("#btnFav").click(() => {
    let token = $('[name="csrfmiddlewaretoken"]').val();
    $.post( "/stockDetails/", { csrfmiddlewaretoken: token, fav:1 } );
});
$("#btnUnfav").click(() => {
    let token = $('[name="csrfmiddlewaretoken"]').val();
    $.post( "/stockDetails/", { csrfmiddlewaretoken: token, fav:0 } );
});
