# src/components/analise_gastos.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Para evitar problemas com backend em alguns sistemas

def render_analise_gastos(df):
    """Renderiza análise detalhada dos gastos"""
    if df.empty:
        st.info("Adicione suas transações para ver a análise detalhada.")
        return
    
    st.subheader("Análise de Gastos")
    
    # Faz uma cópia para não modificar o DataFrame original
    df = df.copy()
    
    # Converte data
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"])
    
    # Métricas principais
    total_gastos = df[df["valor"] < 0]["valor"].sum()
    total_ganhos = df[df["valor"] > 0]["valor"].sum()
    saldo = total_ganhos + total_gastos
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Ganhos", f"R$ {total_ganhos:,.2f}")
    with col2:
        st.metric("Total Gastos", f"R$ {total_gastos:,.2f}")
    with col3:
        st.metric("Saldo", f"R$ {saldo:,.2f}", 
                  delta=f"{saldo:,.2f}" if saldo != 0 else None)
    with col4:
        st.metric("Qtd. Transações", len(df))
    
    # Gráfico de gastos por categoria
    st.subheader("Gastos por Categoria")
    gastos_categoria = df[df["valor"] < 0].groupby("categoria")["valor"].sum().abs()
    
    if not gastos_categoria.empty:
        # Gráfico
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            gastos_categoria.sort_values().plot(kind="barh", ax=ax, color='#ff6b6b')
            ax.set_xlabel("Valor Gasto (R$)", fontsize=12)
            ax.set_title("Distribuição de Gastos por Categoria", fontsize=14, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Formata os valores no eixo x
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
            
            # Ajusta layout para não cortar labels
            plt.tight_layout()
            
            st.pyplot(fig)
            plt.close(fig)  # Fecha a figura para liberar memória
        except Exception as e:
            st.warning(f"Não foi possível gerar o gráfico: {str(e)}")
        
        # Tabela de gastos por categoria
        st.subheader("Detalhamento por Categoria")
        df_categoria = gastos_categoria.reset_index().rename(
            columns={"categoria": "Categoria", "valor": "Total Gasto (R$)"}
        )
        df_categoria["% do Total"] = (df_categoria["Total Gasto (R$)"] / abs(total_gastos) * 100).round(1).astype(str) + "%"
        df_categoria = df_categoria.sort_values("Total Gasto (R$)", ascending=False)
        
        st.dataframe(
            df_categoria,
            use_container_width=True,
            hide_index=True
        )
    
    # Análise de receitas
    receitas_categoria = df[df["valor"] > 0].groupby("categoria")["valor"].sum()
    if not receitas_categoria.empty:
        st.subheader("Receitas por Categoria")
        df_receitas = receitas_categoria.reset_index().rename(
            columns={"categoria": "Categoria", "valor": "Total Receita (R$)"}
        )
        st.dataframe(df_receitas, use_container_width=True, hide_index=True)
    
    # Padrões identificados
    st.subheader("Padrões Identificados")
    
    col_padroes1, col_padroes2 = st.columns(2)
    
    with col_padroes1:
        # Maior gasto
        if not df[df["valor"] < 0].empty:
            maior_gasto = df[df["valor"] < 0].loc[df[df["valor"] < 0]["valor"].idxmin()]
            st.info(f"**Maior gasto:** {maior_gasto['descricao']}\n\nR$ {abs(maior_gasto['valor']):,.2f}")
        
        # Categoria mais frequente
        if not df[df["valor"] < 0].empty:
            categoria_freq = df[df["valor"] < 0]["categoria"].mode()[0]
            st.info(f"**Categoria mais frequente:** {categoria_freq.capitalize()}")
    
    with col_padroes2:
        # Ticket médio
        if not df[df["valor"] < 0].empty:
            ticket_medio = abs(df[df["valor"] < 0]["valor"].mean())
            st.info(f"**Ticket médio:** R$ {ticket_medio:,.2f}")
        
        # Número de dias com gastos
        if "data" in df.columns and not df[df["valor"] < 0].empty:
            dias_com_gastos = df[df["valor"] < 0]["data"].nunique()
            total_dias = (df["data"].max() - df["data"].min()).days + 1 if len(df) > 1 else 1
            if total_dias > 0:
                st.info(f"**Dias com gastos:** {dias_com_gastos} de {total_dias} dias ({dias_com_gastos/total_dias*100:.0f}%)")
    
    # Análise de tendência de gastos
    if "data" in df.columns and len(df) >= 7:
        st.subheader("Tendência de Gastos")
        
        # Agrupa por dia
        df_diario = df[df["valor"] < 0].groupby(df["data"].dt.date)["valor"].sum().abs().reset_index()
        df_diario.columns = ["data", "gastos"]
        df_diario = df_diario.sort_values("data")
        
        if len(df_diario) >= 2:
            try:
                fig2, ax2 = plt.subplots(figsize=(10, 4))
                ax2.plot(df_diario["data"], df_diario["gastos"], marker='o', linestyle='-', color='#4ecdc4')
                ax2.set_xlabel("Data", fontsize=12)
                ax2.set_ylabel("Gastos (R$)", fontsize=12)
                ax2.set_title("Evolução Diária de Gastos", fontsize=14, fontweight='bold')
                ax2.grid(True, alpha=0.3)
                
                # Formata eixo y
                ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
                
                # Rotaciona labels do eixo x
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                st.pyplot(fig2)
                plt.close(fig2)
            except Exception as e:
                st.warning(f"Não foi possível gerar o gráfico de tendência: {str(e)}")
        
        # Análise de comparação de períodos
        df_sorted = df.sort_values("data")
        ultimos_7 = df_sorted.tail(7)
        anteriores = df_sorted.head(len(df_sorted) - 7)
        
        gastos_ultimos = ultimos_7[ultimos_7["valor"] < 0]["valor"].sum() if not ultimos_7.empty else 0
        gastos_anteriores = anteriores[anteriores["valor"] < 0]["valor"].sum() if not anteriores.empty else 0
        
        if gastos_anteriores != 0 and gastos_ultimos != 0:
            variacao = ((abs(gastos_ultimos) - abs(gastos_anteriores)) / abs(gastos_anteriores)) * 100
            
            col_var1, col_var2 = st.columns(2)
            with col_var1:
                st.metric(
                    "Últimos 7 dias", 
                    f"R$ {abs(gastos_ultimos):,.2f}",
                    delta=f"{variacao:+.1f}%"
                )
            with col_var2:
                st.metric(
                    "Período anterior", 
                    f"R$ {abs(gastos_anteriores):,.2f}"
                )
            
            if variacao > 10:
                st.warning(f"Seus gastos aumentaram **{variacao:.1f}%** nos últimos 7 dias. Considere revisar seus gastos.")
            elif variacao < -10:
                st.success(f"Seus gastos diminuíram **{abs(variacao):.1f}%** nos últimos 7 dias. Ótimo trabalho!")
            else:
                st.info(f"Seus gastos estão estáveis com variação de **{variacao:.1f}%** nos últimos 7 dias.")
    
    # Resumo financeiro em texto
    st.subheader("Resumo Financeiro")
    
    if not df.empty:
        resumo = []
        resumo.append(f"Período analisado: {df['data'].min().strftime('%d/%m/%Y')} a {df['data'].max().strftime('%d/%m/%Y')}")
        resumo.append(f"Total de receitas: R$ {total_ganhos:,.2f}")
        resumo.append(f"Total de despesas: R$ {abs(total_gastos):,.2f}")
        
        if total_ganhos > 0:
            taxa_poupanca = (abs(total_gastos) / total_ganhos) * 100
            if taxa_poupanca < 50:
                resumo.append(f"Taxa de poupança: {100 - taxa_poupanca:.1f}% (Excelente!)")
            elif taxa_poupanca < 70:
                resumo.append(f"Taxa de poupança: {100 - taxa_poupanca:.1f}% (Bom, mas pode melhorar)")
            else:
                resumo.append(f"Taxa de poupança: {100 - taxa_poupanca:.1f}% (Atenção! Considere reduzir gastos)")
        
        for linha in resumo:
            st.write(linha)