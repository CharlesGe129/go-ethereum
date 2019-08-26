package jsong

import (
	"github.com/ethereum/go-ethereum/core/types"
	"sync"
	"time"
)

var (
	once  sync.Once
	queue *BlockQueue
)

func GetBlockQueue() *BlockQueue {
	once.Do(func() {
		queue := &BlockQueue{
			blocks: make([]BlockWithSigner, 0),
		}
		go func() {
			time.Sleep(time.Second)
			for len(queue.blocks) > 0 {
				bs := queue.DeQueue()
				BlockToFile(bs.Block, bs.Signer)
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
	blocks []BlockWithSigner
	mux    sync.Mutex
}

func (queue *BlockQueue) EnQueue(b *types.Block, signer *types.Signer) {
	queue.mux.Lock()
	queue.blocks = append(queue.blocks, BlockWithSigner{
		Block:  b,
		Signer: signer,
	})
	queue.mux.Unlock()
}

func (queue *BlockQueue) DeQueue() BlockWithSigner {
	queue.mux.Lock()
	bs := queue.blocks[0]
	queue.blocks = queue.blocks[1:]
	queue.mux.Unlock()
	return bs
}
