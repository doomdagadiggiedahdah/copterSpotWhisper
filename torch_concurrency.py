import torch
import torch.multiprocessing as mp
import time

class SimpleModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(10, 1)
    
    def forward(self, x):
        return self.linear(x)

def worker_job(worker_id, files, device):
    print(f"Worker {worker_id} starting on {device}...")
    
    model = SimpleModel().to(device)
    
    for file in files:
        fake_data = torch.randn(1, 10, device=device)  # Create random tensor
        
        with torch.no_grad():  # No need for gradients in inference
            output = model(fake_data)
            
        time.sleep(1)  # Simulate additional processing
        print(f"Worker {worker_id} processed {file} - Output: {output.item():.4f}")
    
    print(f"Worker {worker_id} finished!")

def main():
    mp.set_start_method('spawn', force=True)
    
    all_files = [f"file_{i}.mp3" for i in range(6)]
    
    worker1_files = all_files[:3]
    worker2_files = all_files[3:]
    
    # Check if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Create worker processes
    p1 = mp.Process(target=worker_job, args=(1, worker1_files, device))
    p2 = mp.Process(target=worker_job, args=(2, worker2_files, device))
    
    # Start both processes
    print("Starting workers...")
    p1.start()
    time.sleep(.5)
    p2.start()
    
    # Wait for both to finish
    p1.join()
    p2.join()
    print("All workers finished!")

if __name__ == "__main__":
    main()