$('#add_product_btn').on('click', requestAddProduct);
$('.off_product_btn').on('click', requestOffProduct);


$('.menu_btn').on('click', function(){
	$('.menu_btn').removeClass('menu_btn_active')
	if($(this).hasClass('menu_all_prod')) {
		$('.menu_all_prod').addClass('menu_btn_active')
		$('.all_products').css('display', 'block')
		$('.discounted_products').css('display', 'none')
	} else {
		$('.menu_discounted').addClass('menu_btn_active')
		$('.all_products').css('display', 'none')
		$('.discounted_products').css('display', 'block')
	}
})


function requestAddProduct() {
	title = $('#inp_product_title').val()
	count = $('#inp_product_count').val()
	date = $('#inp_date_for_off').val()
	status = "product"
	if (title.length > 0 && count.length > 0 && date.length > 0) {
		$.ajax({
            url: '/warehouse/add_product',        
            method: 'post',             
            dataType: 'json',         
            data: {
                title: title,
                count: count,
                date: date,
                status: status
            },    
            success: function(returned_prod_id){   
            	if (returned_prod_id == 0) {
	                console.log("returned_prod_id = 0")
                    return false
                } else {
                    $('.products_block_wrapper').prepend(
                		$("<div>", {class: "product_block"})
                			.append("<div class='product_id'>"+returned_prod_id+"</div>")
                			.append("<div class='product_title'>"+title+"</div>")
                			.append("<div class='product_count'>Количество: "+ count+" шт</div>")
                			.append("<div class='date_for_off'>Конец срока годности: "+ date + "</div>")
                			.append("<div class='btn_for_discount'><button class='off_product_btn'>Удалить со склада</button></div>")
                	)
                	$('#inp_product_title').val('')
                	$('#inp_product_count').val('')
                	$('#inp_date_for_off').val('')
                }
            }
        });
	}
}

function requestOffProduct() {
	prod_id = $(this).parent().parent().children()[0].innerText
	status = "off"
	$.ajax({
            url: '/warehouse/update_product_status',        
            method: 'post',             
            dataType: 'json',         
            data: {
                prod_id: prod_id,
                status: status
            },    
            success: function(data){   
                console.log("requestOffProduct: " + data);       
            }
        });
	$(this).parent().parent().remove()
}