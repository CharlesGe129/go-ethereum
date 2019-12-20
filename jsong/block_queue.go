package jsong

import (
	"sync"
	"time"

	"github.com/ethereum/go-ethereum/core/types"
)

var (
	blockOnce  sync.Once
	blockQueue *BlockQueue
)

func GetBlockQueue() *BlockQueue {
	blockOnce.Do(func() {
		blockQueue = &BlockQueue{
			blocks: make(chan BlockWithSigner, 128),
		}
		go func() {
			for {
				select {
				case bs := <-blockQueue.blocks:
					BlockToFile(bs.Block, bs.Signer, bs.TimeNow)
				}
			}
		}()
	})
	return blockQueue
}

type BlockWithSigner struct {
	Block   *types.Block
	Signer  *types.Signer
	TimeNow string
}

type BlockQueue struct {
	blocks chan BlockWithSigner
}

func (queue *BlockQueue) EnQueue(b *types.Block, signer *types.Signer) {
	queue.blocks <- BlockWithSigner{
		Block:   b,
		Signer:  signer,
		TimeNow: time.Now().String(),
	}
}

func (queue *BlockQueue) DeQueue() BlockWithSigner {
	return <-queue.blocks
}
