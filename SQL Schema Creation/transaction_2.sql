USE [Customers_Detail]
GO

/****** Object:  Table [dbo].[transaction_2]    Script Date: 07/07/2020 03:00:48 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[transaction_2](
	[id_transaction] [int] NOT NULL,
	[id_account] [int] NOT NULL,
	[type] [nvarchar](50) NULL,
	[date] [nvarchar](50) NULL,
	[amount] [float] NOT NULL,
	[month] [nvarchar](50) NULL,
 CONSTRAINT [PK_transaction_2] PRIMARY KEY CLUSTERED 
(
	[id_transaction] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


