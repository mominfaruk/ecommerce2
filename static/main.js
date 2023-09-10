var shoppingCart = (function () {
  cart = [];

  function Item(id, name, price, count) {
    this.id = id;
    this.name = name;
    this.price = price;
    this.count = count;
  }

  // Save cart
  function saveCart() {
    localStorage.setItem("shoppingCart", JSON.stringify(cart));
  }

  // Load cart
  function loadCart() {
    cart = JSON.parse(localStorage.getItem("shoppingCart"));
  }
  if (localStorage.getItem("shoppingCart") != null) {
    loadCart();
  }

  var obj = {};

  obj.initialise = function (id, name, price, count) {
    for (var item in cart) {
      if (cart[item].name === name) {
        cart[item].count = count;
        saveCart();
        return;
      }
    }
    var item = new Item(id, name, price, count);
    cart.push(item);
    saveCart();
    displayCart();
  };
  // Add to cart
  obj.addItemToCart = function (id, name, price, count) {
    console.log("add to cart");
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    console.log(id, name, price, count);
    $.ajax({
      url: "/add_to_cart/",
      type: "POST",
      data: JSON.stringify({ product_id: id, price: price, quantity: count }),
      dataType: "json",
      contentType: "application/json",
      headers: { "X-CSRFToken": csrfToken },
      success: function (data) {
        console.log(data);
      },
      error: function (error) {
        console.log(error);
      },
    });
    for (var item in cart) {
      if (cart[item].name === name) {
        cart[item].count++;
        saveCart();
        return;
      }
    }
    var item = new Item(id, name, price, count);
    cart.push(item);
    saveCart();

    // Now, also send this item to the backend
  };

  // Remove item from cart
  obj.removeItemFromCart = function (name) {
    for (var item in cart) {
      if (cart[item].name === name) {
        cart[item].count--;
        if (cart[item].count <= 0) {
          removeBackendCartItem(cart[item]);
          cart.splice(item, 1);
        } else {
          updateBackendCartItem(cart[item]);
        }
        break;
      }
    }
    saveCart();
  };

  // Set count for item
  obj.setCountForItem = function (name, count) {
    for (var item in cart) {
      if (cart[item].name === name) {
        cart[item].count = count;
        if (cart[item].count <= 0) {
          removeBackendCartItem(cart[item]);
          cart.splice(item, 1);
        } else {
          updateBackendCartItem(cart[item]);
        }
        break;
      }
    }
    saveCart();
  };
  function removeBackendCartItem(item) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
      url: "/remove_from_cart/",
      type: "POST",
      data: JSON.stringify({ product_id: item.id }),
      dataType: "json",
      contentType: "application/json",
      headers: { "X-CSRFToken": csrfToken },
      success: function (data) {
        console.log(data);
      },
      error: function (error) {
        console.log(error);
      },
    });
  }

  // Update cart item in the backend
  function updateBackendCartItem(item) {
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
      url: "/update_cart/",
      type: "POST",
      data: JSON.stringify({ product_id: item.id, quantity: item.count }),
      dataType: "json",
      contentType: "application/json",
      headers: { "X-CSRFToken": csrfToken },
      success: function (data) {
        console.log("Updated");
      },
      error: function (error) {
        console.log(error);
      },
    });
  }

  // Remove all items from cart
  obj.removeItemFromCartAll = function (name) {
    for (var item in cart) {
      if (cart[item].name === name) {
        cart.splice(item, 1);
        removeBackendCartItem(cart[item]);
        break;
      }
    }
    saveCart();
  };
  obj.removeItemFromCart = function (name) {
    for (var item in cart) {
      if (cart[item].name === name) {
        cart.splice(item, 1);
        break;
      }
    }
    saveCart();
  };

  // Clear cart
  obj.clearCart = function () {
    cart = [];
    saveCart();
  };

  // Count cart
  obj.totalCount = function () {
    var totalCount = 0;
    for (var item in cart) {
      totalCount += cart[item].count;
    }
    return totalCount;
  };

  // Total cart
  obj.totalCart = function () {
    var totalCart = 0;
    for (var item in cart) {
      var itemTotal = cart[item].price * cart[item].count;
      if (itemTotal > 0) {
        totalCart += itemTotal;
      }
    }
    return Number(totalCart.toFixed(2));
  };
  obj.clearCartItems = function () {
    cart = [];
    saveCart();
  };

  // List cart
  obj.listCart = function () {
    var cartCopy = [];
    for (i in cart) {
      item = cart[i];
      itemCopy = {};
      for (p in item) {
        itemCopy[p] = item[p];
      }
      itemCopy.total = Number(item.price * item.count).toFixed(2);
      cartCopy.push(itemCopy);
    }
    return cartCopy;
  };
  return obj;
})();

// Add item
$(".adding").click(function (event) {
  // alert('working');
  event.preventDefault();
  var id = $(this).data("id");
  var name = $(this).data("name").replace(/_/g, " ");
  var price = Number($(this).data("price"));
  shoppingCart.addItemToCart(id, name, price, 1);
  displayCart();
});

// Clear items
$(".clear-cart").click(function () {
  shoppingCart.clearCart();
  displayCart();
});

function displayCart() {
  var cartArray = shoppingCart.listCart();
  var output = "";
  var totalCount = 0;
  for (var i in cartArray) {
    var name = String(cartArray[i].name).replace(/_/g, " ");
    if (cartArray[i].count <= 0) {
      // Skip the item if the count is 0 or negative
      continue;
    }
    totalCount += cartArray[i].count;
    output +=
      "<tr>" +
      "<td>" +
      name +
      "</td>" +
      "<td>(" +
      cartArray[i].price +
      ")</td>" +
      "<td><div class='input-group'>" +
      "<input type='number' class='item-count form-control' data-name='" +
      name.replace(/ /g, "_") +
      "' value='" +
      cartArray[i].count +
      "'>" +
      "</div></td>" +
      "<td><button class='delete-item btn btn-danger'  data-id='" +
      cartArray[i].id +
      "' data-name=" +
      name.replace(/ /g, "_") +
      ">X</button></td>" +
      " = " +
      "<td>" +
      cartArray[i].total +
      "</td>" +
      "</tr>";
  }
  $(".show-cart").html(output);

  // Update the total count in the navbar
  if (totalCount <= 0) {
    $(".total-count").html("");
  } else {
    $(".total-count").html(totalCount);
  }
  if (totalCount > 0) {
    $("#buyNowButton").show();
  } else {
    $("#buyNowButton").hide();
  }

  $(".total-cart").html(shoppingCart.totalCart());
}

// Delete item button

$(".show-cart").on("click", ".delete-item", function (event) {
  var id = $(this).data("id");
  var name = $(this).data("name").replace(/_/g, " ");
  for (var i = 0; i < cart.length; i++) {
    if (cart[i].id === id) {
      shoppingCart.removeItemFromCart(name);
      break;
    }
  }
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajax({
    url: "/remove_from_cart/",
    type: "POST",
    data: JSON.stringify({ product_id: id }), // Updated to use 'id' instead of 'item.id'
    dataType: "json",
    contentType: "application/json",
    headers: { "X-CSRFToken": csrfToken },
    success: function (data) {
      console.log(data);
    },
    error: function (error) {
      console.log(error);
    },
  });

  displayCart();
});

// Item count input
$(".show-cart").on("change", ".item-count", function (event) {
  var name = $(this).data("name").replace(/_/g, " ");
  var count = Number($(this).val());
  shoppingCart.setCountForItem(name, count);
  displayCart();
});
displayCart();

//////// ui script start /////////
// Tabs Single Page
$(".tab ul.tabs").addClass("active").find("> li:eq(0)").addClass("current");
$(".tab ul.tabs li a").on("click", function (g) {
  var tab = $(this).closest(".tab"),
    index = $(this).closest("li").index();
  tab.find("ul.tabs > li").removeClass("current");
  $(this).closest("li").addClass("current");
  tab
    .find(".tab_content")
    .find("div.tabs_item")
    .not("div.tabs_item:eq(" + index + ")")
    .slideUp();
  tab
    .find(".tab_content")
    .find("div.tabs_item:eq(" + index + ")")
    .slideDown();
  g.preventDefault();
});

function loadCartItemsFromBackend() {
  $.ajax({
    url: "/load_cart_items/", // Replace with the path of your new view
    type: "GET",
    dataType: "json",
    success: function (data) {
      console.log(data);
      if (data.cart.length == 0) {
        shoppingCart.clearCartItems();
      } else {
        for (var i = 0; i < data.cart.length; i++) {
          var item = data.cart[i];
          shoppingCart.initialise(item.id, item.name, item.price, item.count);
        }
      }
      displayCart();
    },
    error: function (error) {
      console.log(error);
    },
  });
}

$(document).ready(function () {
  loadCartItemsFromBackend();
});

$("#logout").click(function () {
  shoppingCart.clearCartItems();
});
