package jsong

import (
	"github.com/ethereum/go-ethereum/core/types"
	"sync"
)

var (
	once  sync.Once
	queue *BlockQueue
)

func GetBlockQueue() *BlockQueue {
	once.Do(func() {
		queue = &BlockQueue{
			blocks: make(chan BlockWithSigner, 10),
		}
		go func() {
			for {
				select {
				case bs := <-queue.blocks:
					BlockToFile(bs.Block, bs.Signer)
				}
			}
		}()
	})
	return queue
}

type BlockWithSigner struct {
	Block  *types.Block
	Signer *types.Signer
}

type BlockQueue struct {
	blocks chan BlockWithSigner
}

func (queue *BlockQueue) EnQueue(b *types.Block, signer *types.Signer) {
	queue.blocks <- BlockWithSigner{
		Block:  b,
		Signer: signer,
	}
}

func (queue *BlockQueue) DeQueue() BlockWithSigner {
	return <-queue.blocks
}
