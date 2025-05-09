undefined
    
    def get_data_range(self, start_date=None, end_date=None):
        """
        Obtiene datos de TRM en un rango de fechas
        
        Args:
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            
        Returns:
            DataFrame: Datos filtrados por el rango de fechas
        """
        if self.data is None:
            return None
        
        filtered_data = self.data.copy()
        
        if start_date:
            start_date = pd.to_datetime(start_date)
            filtered_data = filtered_data[filtered_data['fecha'] >= start_date]
            
        if end_date:
            end_date = pd.to_datetime(end_date)
            filtered_data = filtered_data[filtered_data['fecha'] <= end_date]
            
        return filtered_data
    
    def get_statistics(self, start_date=None, end_date=None):
        """
        Calcula estadísticas básicas para un rango de fechas
        
        Args:
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            
        Returns:
            dict: Estadísticas calculadas
        """
        filtered_data = self.get_data_range(start_date, end_date)
        
        if filtered_data is None or filtered_data.empty:
            return None
        
        stats = {
            'min': filtered_data['trm'].min(),
            'max': filtered_data['trm'].max(),
            'avg': filtered_data['trm'].mean(),
            'median': filtered_data['trm'].median(),
            'std': filtered_data['trm'].std(),
            'count': len(filtered_data),
            'start_date': filtered_data['fecha'].min().strftime('%Y-%m-%d'),
            'end_date': filtered_data['fecha'].max().strftime('%Y-%m-%d'),
            'start_value': filtered_data.iloc[0]['trm'],
            'end_value': filtered_data.iloc[-1]['trm'],
            'change': filtered_data.iloc[-1]['trm'] - filtered_data.iloc[0]['trm'],
            'change_pct': (filtered_data.iloc[-1]['trm'] / filtered_data.iloc[0]['trm'] - 1) * 100
        }
        
        return stats
    
    def plot_trm(self, start_date=None, end_date=None, save_path=None):
        """
        Genera un gráfico de la TRM en un rango de fechas
        
        Args:
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            save_path (str): Ruta para guardar el gráfico
            
        Returns:
            matplotlib.figure.Figure: Figura generada
        """
        filtered_data = self.get_data_range(start_date, end_date)
        
        if filtered_data is None or filtered_data.empty:
            return None
        
        plt.figure(figsize=(12, 6))
        plt.plot(filtered_data['fecha'], filtered_data['trm'])
        plt.title('Histórico TRM Colombia')
        plt.xlabel('Fecha')
        plt.ylabel('TRM (COP/USD)')
        plt.grid(True)
        
        # Añadir anotaciones de valores mínimos y máximos
        min_idx = filtered_data['trm'].idxmin()
        max_idx = filtered_data['trm'].idxmax()
        
        plt.annotate(f'Min: {filtered_data.loc[min_idx, "trm"]:.2f}',
                    xy=(filtered_data.loc[min_idx, 'fecha'], filtered_data.loc[min_idx, 'trm']),
                    xytext=(10, -30), textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
        
        plt.annotate(f'Max: {filtered_data.loc[max_idx, "trm"]:.2f}',
                    xy=(filtered_data.loc[max_idx, 'fecha'], filtered_data.loc[max_idx, 'trm']),
                    xytext=(10, 30), textcoords='offset points',
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
        
        if save_path:
            plt.savefig(save_path)
            
        return plt.gcf()
    
    def calculate_moving_average(self, window=30, start_date=None, end_date=None):
        """
        Calcula el promedio móvil de la TRM
        
        Args:
            window (int): Tamaño de la ventana para el promedio móvil
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            
        Returns:
            DataFrame: Datos con el promedio móvil calculado
        """
        filtered_data = self.get_data_range(start_date, end_date)
        
        if filtered_data is None or filtered_data.empty:
            return None
        
        filtered_data[f'ma_{window}'] = filtered_data['trm'].rolling(window=window).mean()
        
        return filtered_data
    
    def find_extreme_variations(self, threshold_pct=1.0, start_date=None, end_date=None):
        """
        Encuentra variaciones extremas en la TRM
        
        Args:
            threshold_pct (float): Umbral de variación porcentual
            start_date (str): Fecha inicial en formato YYYY-MM-DD
            end_date (str): Fecha final en formato YYYY-MM-DD
            
        Returns:
            DataFrame: Datos con variaciones que superan el umbral
        """
        filtered_data = self.get_data_range(start_date, end_date)
        
        if filtered_data is None or filtered_data.empty:
            return None
        
        # Calcular variación diaria
        filtered_data['var_pct'] = filtered_data['trm'].pct_change() * 100
        
        # Filtrar por umbral
        extreme_variations = filtered_data[abs(filtered_data['var_pct']) > threshold_pct].copy()
        
        return extreme_variations

# Ejemplo de uso
if __name__ == "__main__":
    loader = TRMDataLoader()
    print(loader.get_statistics())
    
    # Ejemplo de gráfico
    loader.plot_trm(save_path="trm_historico.png")
    plt.show()