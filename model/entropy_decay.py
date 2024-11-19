from stable_baselines3.common.callbacks import BaseCallback

class EntropyDecayCallback(BaseCallback):
    def __init__(self, initial_entropy_coef, final_entropy_coef, total_timesteps, verbose=0):
        super(EntropyDecayCallback, self).__init__(verbose)
        self.initial_entropy_coef = initial_entropy_coef
        self.final_entropy_coef = final_entropy_coef
        self.total_timesteps = total_timesteps

    def _on_step(self) -> bool:
        # Calculate the linear decay of the entropy coefficient
        progress = min(1.0, self.num_timesteps / self.total_timesteps)
        current_entropy_coef = self.initial_entropy_coef - progress * (self.initial_entropy_coef - self.final_entropy_coef)

        # Set the new entropy coefficient
        self.model.ent_coef = current_entropy_coef

        if self.verbose > 0:
            print(f"Step: {self.num_timesteps}, Entropy Coef: {current_entropy_coef}")
        
        return True