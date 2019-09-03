package jsong

import (
	"encoding/hex"
	"fmt"
	"github.com/ethereum/go-ethereum/core/types"
	"os"
	"strings"
	"time"
)

func TxToFile(tx *types.Transaction, localAddr, remoteAddr, timeNow string) {
	contentToRecord := TxToJson(tx, localAddr, remoteAddr)
	recordTx(contentToRecord, timeNow)
}

func BlockToFile(block *types.Block, signer *types.Signer, timeNow string) {
	contentToRecord := BlockToJson(block)
	var from, to string
	for _, tx := range block.Transactions() {
		v, r, s := tx.RawSignatureValues()
		msg, err := tx.AsMessage(*signer)
		if err != nil {
			from = "error"
		} else {
			from = msg.From().String()
		}
		if tx.To() == nil {
			to = ""
		} else {
			to = tx.To().String()
		}
		// Cost returns amount + gasprice * gaslimit.
		contentToRecord += fmt.Sprintf("tx hash=%s, from=%s, to=%s, gasPrice=%v, "+
			"ammount=%v, gas=%v, nonce=%v, payload=%s, "+
			"checkNonce=%v, signV=%v, signR=%v, signS=%v, "+
			"chainId=%v, protected=%v, size=%s, cost=%v\n",
			tx.Hash().String(), from, to, tx.GasPrice(),
			tx.Value(), tx.Gas(), tx.Nonce(), hex.EncodeToString(tx.Data()),
			tx.CheckNonce(), v, r, s,
			tx.ChainId(), tx.Protected(), tx.Size().String(), tx.Cost())
	}

	recordBlock(contentToRecord, timeNow)
}

func recordTx(content string, now string) {
	timeList := strings.Split(now, " ")
	timeNow := timeList[0] + "_" + strings.Split(timeList[1], ":")[0]
	filename := "records/txs/" + strings.Split(timeNow, " ")[0] + ".txt"
	appendToFile(filename, "["+time.Now().String()+"] "+content+"\n")
}

func recordBlock(content string, now string) {
	timeNow := strings.Split(now, " ")[0]
	filename := "records/blocks/" + strings.Split(timeNow, " ")[0] + ".txt"
	appendToFile(filename, fmt.Sprintf("[%s] %s\n", now, content))
}

func appendToFile(fileName string, content string) error {
	// 以只写的模式，打开文件
	f, err := os.OpenFile(fileName, os.O_WRONLY, 0644)
	if err != nil {
		os.Create(fileName)
		f, err = os.OpenFile(fileName, os.O_WRONLY, 0644)
	}

	// 查找文件末尾的偏移量
	n, _ := f.Seek(0, os.SEEK_END)
	// 从末尾的偏移量开始写入内容
	_, err = f.WriteAt([]byte(content), n)

	defer f.Close()
	return err
}
