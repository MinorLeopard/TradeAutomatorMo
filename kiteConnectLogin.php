<?php
    require_once __DIR__ . '/vendor/autoload.php';

    use KiteConnect\KiteConnect;

    // Initialise.
    $kite = new KiteConnect("389m4rmjkmdp05p1");

    // Assuming you have obtained the `request_token`
    // after the auth flow redirect by redirecting the
    // user to $kite->login_url()
    try {
        $user = $kite->generateSession("request_token_obtained", "your_api_secret");
        echo "Authentication successful. \n";
        print_r($user);
        $kite->setAccessToken($user->access_token);
    } catch(Exception $e) {
        echo "Authentication failed: ".$e->getMessage();
        throw $e;
    }

    echo $user->user_id." has logged in";

    // Get the list of positions.
    echo "Positions: \n";
    print_r($kite->getPositions());

    // Place order.
    $order = $kite->placeOrder("regular", [
        "tradingsymbol" => "INFY",
        "exchange" => "NSE",
        "quantity" => 1,
        "transaction_type" => "BUY",
        "order_type" => "MARKET",
        "product" => "NRML"
    ]);

    echo "Order id is ".$order->order_id;
?>