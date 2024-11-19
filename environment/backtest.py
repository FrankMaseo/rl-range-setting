import matplotlib.pyplot as plt
import pandas as pd

def backtest_model(env, model, chart_title=None):
    env._eval()
    
    timestamps = []
    price_series = []
    lower_bound_series = []
    upper_bound_series = []
    data = []
    
    
    obs, _ = env.reset()

    done = False
    
    additional_text = chart_title + ' - ' if chart_title else ""
    
    while not done:
        from_step = env.current_step
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, _, _ = env.step(action)
        to_step = env.current_step

        lower_bound = env.liquidity_range.lower_bound
        upper_bound = env.liquidity_range.upper_bound

        # Record the data
        data.append({
            'from_step': from_step,
            'to_step': to_step,
            'total_rewards': reward,
            'liquidity_range_low': lower_bound,
            'liquidity_range_high': upper_bound
        })
        
    df_results_raw = pd.DataFrame(data)
    liq_columns = ['liquidity_range_low', 'liquidity_range_high']
    df_results_flat = pd.DataFrame(index=range(0,df_results_raw.to_step.max()), columns=liq_columns+['rewards'])
    for i,r in df_results_raw.iterrows(): 
        for range_col in liq_columns:
            df_results_flat.loc[r['from_step']:r['to_step']+1, range_col] = r[range_col]
        #set rewards
        df_results_flat.loc[r['from_step']:r['to_step']+1, 'rewards'] = (r['total_rewards']+env.PENALTIES['range_change']) / (r['to_step']-r['from_step']+1)
        df_results_flat.loc[r['from_step'], 'rewards'] -= env.PENALTIES['range_change']

    df_results = env.price_data.copy()
    df_results[liq_columns+['rewards']] = df_results_flat[liq_columns+['rewards']]
    df_results.plot(y=['close', 'liquidity_range_low', 'liquidity_range_high'], title=f'{additional_text}Price chart with predicted ranges' , figsize=(30,18))
    df_results['cum_rewards'] = df_results.rewards.cumsum()
    df_results.plot( y='cum_rewards', title=f'{additional_text}Total rewards over time', figsize=(10,6))

    df_results['range_width'] = df_results.liquidity_range_high-df_results.liquidity_range_low
    df_results['max_range_width'] = env.max_range_width

    df_results.plot(y=['range_width', 'max_range_width'], title=f'{additional_text}Range width over time')
    print(f'{additional_text}Total range changes over {df_results_raw.to_step.max() - df_results_raw.from_step.min()} days: {df_results_raw.liquidity_range_low.count()}')
    print(f'{additional_text}Average liquidity lifespan: {(df_results_raw.to_step.max() - df_results_raw.from_step.min())/df_results_raw.liquidity_range_low.count()} days')
    
    total_rewards = df_results_raw.total_rewards.sum()
    range_changes = df_results_raw.liquidity_range_low.count()
    total_periods = df_results_raw.to_step.max() - df_results_raw.from_step.min()
    
    return total_rewards, range_changes, total_periods