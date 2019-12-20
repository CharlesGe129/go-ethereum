package jsong

import (
	"sync"
	"time"

	"github.com/ethereum/go-ethereum/core/types"
)

var (
	txOnce  sync.Once
	txQueue *TxQueue
)

func GetTxQueue() *TxQueue {
	txOnce.Do(func() {
		txQueue = &TxQueue{
			txs: make(chan TxWithAddr, 1024),
		}
		go func() {
			for {
				select {
				case tx := <-txQueue.txs:
					TxToFile(tx.Transaction, tx.PeerLocalAddr, tx.PeerRemoteAddr, tx.TimeNow)
				}
			}
		}()
	})
	return txQueue
}

type TxWithAddr struct {
	Transaction    *types.Transaction
	PeerLocalAddr  string
	PeerRemoteAddr string
	TimeNow        string
}

type TxQueue struct {
	txs chan TxWithAddr
}

func (queue *TxQueue) EnQueue(tx *types.Transaction, peerLocalAddr, peerRemoteAddr string) {
	queue.txs <- TxWithAddr{
		Transaction:    tx,
		PeerLocalAddr:  peerLocalAddr,
		PeerRemoteAddr: peerRemoteAddr,
		TimeNow:        time.Now().String(),
	}
}

func (queue *TxQueue) DeQueue() TxWithAddr {
	return <-queue.txs
}
