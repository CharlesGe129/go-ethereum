package jsong

import (
	"encoding/hex"
	"encoding/json"

	"github.com/ethereum/go-ethereum/core/types"
)

type Transaction struct {
	Hash           string `json:"hash"`
	To             string `json:"to"`
	GasPrice       string `json:"gas_price"`
	Amount         string `json:"amount"`
	GasLimit       uint64 `json:"gas_limit"`
	Nonce          uint64 `json:"nonce"`
	Payload        string `json:"payload"`
	CheckNonce     bool   `json:"check_nonce"`
	SignV          string `json:"sign_v"`
	SignR          string `json:"sign_r"`
	SignS          string `json:"sign_s"`
	PeerLocalAddr  string `json:"peer_local_addr"`
	PeerRemoteAddr string `json:"peer_remote_addr"`
	ChainId        string `json:"chain_id"`
	Protected      bool   `json:"protected"`
	Size           string `json:"size"`
	Cost           string `json:"cost"`
}

func TxToJson(transaction *types.Transaction, localAddr, remoteAddr string) string {
	var to string
	if transaction.To() == nil {
		to = ""
	} else {
		to = transaction.To().String()
	}
	v, r, s := transaction.RawSignatureValues()
	// Cost returns amount + gasprice * gaslimit.
	tx := Transaction{
		Hash:     transaction.Hash().String(),
		To:       to,
		GasPrice: transaction.GasPrice().String(),
		Amount:   transaction.Value().String(),
		GasLimit: transaction.Gas(),
		Nonce: transaction.Nonce(),
		Payload: hex.EncodeToString(transaction.Data()),
		CheckNonce: transaction.CheckNonce(),
		SignV: v.String(),
		SignR: r.String(),
		SignS: s.String(),
		PeerLocalAddr: localAddr,
		PeerRemoteAddr: remoteAddr,
		ChainId: transaction.ChainId().String(),
		Protected: transaction.Protected(),
		Size: transaction.Size().String(),
		Cost: transaction.Cost().String(),
	}
	body, err := json.Marshal(tx)
	if err != nil {
		return err.Error() + "\n"
	} else {
		return string(body) + "\n"
	}
}

type Block struct {
	Hash            string   `json:"hash"`
	ParentHash      string   `json:"parentHash"`
	UncleHash       string   `json:"uncleHash"`
	ReceiptHash     string   `json:"receiptHash"`
	Nonce           uint64   `json:"nonce"`
	LogsBloom       string   `json:"logsBloom"`
	Number          string   `json:"number"`
	Miner           string   `json:"miner"`
	Uncles          []string `json:"uncles"`
	TxNum           int      `json:"txNum"`
	GasUsed         uint64   `json:"gasUsed"`
	GasLimit        uint64   `json:"gasLimit"`
	Difficulty      string   `json:"difficulty"`
	Root            string   `json:"root"`
	MixDigest       string   `json:"mixDigest"`
	Size            string   `json:"size"`
	TotalDifficulty string   `json:"totalDifficulty"`
	Extra           string   `json:"extra"`
	Timestamp       uint64   `json:"timestamp"`
}

func BlockToJson(block *types.Block) string {
	uncles := make([]string, 0)
	for _, uncle := range block.Uncles() {
		uncles = append(uncles, uncle.Hash().String())
	}
	b := Block{
		Hash:            block.Hash().String(),
		ParentHash:      block.ParentHash().String(),
		UncleHash:       block.UncleHash().String(),
		ReceiptHash:     block.ReceiptHash().String(),
		Nonce:           block.Nonce(),
		LogsBloom:       hex.EncodeToString(block.Bloom().Bytes()),
		Number:          block.Number().String(),
		Miner:           block.Header().Coinbase.String(),
		Uncles:          uncles,
		TxNum:           len(block.Transactions()),
		GasUsed:         block.GasUsed(),
		GasLimit:        block.GasLimit(),
		Difficulty:      block.Difficulty().String(),
		Root:            block.Root().String(),
		MixDigest:       block.MixDigest().String(),
		Size:            block.Size().String(),
		TotalDifficulty: block.DeprecatedTd().String(),
		Extra:           hex.EncodeToString(block.Extra()),
		Timestamp:       block.Time(),
	}
	s, err := json.Marshal(b)
	if err != nil {
		return err.Error() + "\n"
	} else {
		return string(s) + "\n"
	}
}
