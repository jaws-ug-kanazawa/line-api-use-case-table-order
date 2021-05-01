<template>
    <v-app class="table-order-font-size">
        <v-app-bar app class="elevation-1">
            <v-toolbar-title>
                <span style="">{{ $t("paymentCompleted.title") }}</span>
            </v-toolbar-title>
        </v-app-bar>
        <v-container v-show="success">
            <v-row justify="center" align-content="center">
                <v-col align="center" class="mt-15">
                    <p class="text-h5"><v-icon large color="success">done</v-icon>{{ $t("paymentCompleted.msg001") }}</p>
                    <v-divider class="mt-1 mb-5"></v-divider>
                    <p>{{ $t("paymentCompleted.msg002") }}</p>
                    <div>
                        <img src="~/assets/img/line_pay2.png" alt="LINE Pay" v-show="linepay">
                        <img src="~/assets/img/paypay.png" alt="Pay Pay" width="50%" height="50%" v-show="paypay">
                    </div>
                    <v-btn color="#00B900" class="white--text ma-5" width="200px" v-on:click="$router.push('/')">
                        <v-icon>house</v-icon><span>&nbsp;{{ $t("paymentCompleted.msg003") }}</span>
                    </v-btn>

                </v-col>
            </v-row>
        </v-container>
    </v-app>
</template>
<script>
/**
 * 決済完了画面
 * 
 */
export default {
    layout: "tableorder/order",
    async asyncData({ app, store, query, $axios, route }) {
        // スタッフ呼び出しの場合
        let linepay = false
        let paypay = false
        if(typeof query["orderId"] === "undefined") {
            store.commit("paymentId", null);
            return {
                success: true,
                linepay: linepay,
                paypay: paypay,
            }
        } else if (typeof query["transactionId"] === "undefined") {
            linepay = false
            paypay = true
        } else if (query["transactionId"]) {
            linepay = true
            paypay = false
        }
        // 決済完了API呼び出し(Payから返ってくるパラメータを渡す)
        const transactionId = query["transactionId"];
        const paymentId = query["orderId"];
        
        let isPaymentError = null
        
        if (linepay) {
            isPaymentError = await app.$tableorder.confirmPayment(transactionId, paymentId);
        } else if (paypay) {
            isPaymentError = await app.$tableorder.getPaymentDetails(paymentId);
        }

        let success = true;
        if (isPaymentError) {
            success = false;
            store.commit("paymentError", true);
        } else {
            store.commit("paymentId", null);
        }

        return {
            success: success,
            linepay: linepay,
            paypay: paypay,
        }
    },
    head() {
        return {
            title: this.$t("title")
        }
    },
    data() {
        return {
            success: null,
            linepay: null,
            paypay: null,
        }
    },
}
</script>