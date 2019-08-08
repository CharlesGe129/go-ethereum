package jsong

import (
	"encoding/hex"
	"encoding/json"

	"github.com/ethereum/go-ethereum/core/types"
)

type Transaction struct {
	//
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
	var uncles []string
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
