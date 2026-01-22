USE [Smart_librarian_users]
GO

/****** Object:  Table [dbo].[logs]    Script Date: 10/16/2025 6:39:27 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[logs](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[user_id] [uniqueidentifier] NULL,
	[action] [nvarchar](100) NOT NULL,
	[metadata] [nvarchar](max) NULL,
	[created_at] [datetime2](3) NOT NULL,
	[meta] [nvarchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[logs] ADD  DEFAULT (sysutcdatetime()) FOR [created_at]
GO
USE [Smart_librarian_users]
GO

/****** Object:  Table [dbo].[favorites]    Script Date: 10/16/2025 6:39:17 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[favorites](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[user_id] [uniqueidentifier] NOT NULL,
	[book_title] [nvarchar](400) NOT NULL,
	[note] [nvarchar](500) NULL,
	[created_at] [datetime2](3) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[favorites] ADD  DEFAULT (sysutcdatetime()) FOR [created_at]
GO

ALTER TABLE [dbo].[favorites]  WITH CHECK ADD  CONSTRAINT [FK_favorites_user] FOREIGN KEY([user_id])
REFERENCES [dbo].[users] ([id])
ON DELETE CASCADE
GO

ALTER TABLE [dbo].[favorites] CHECK CONSTRAINT [FK_favorites_user]
GO


USE [Smart_librarian_users]
GO

/****** Object:  Table [dbo].[conversations]    Script Date: 10/16/2025 6:39:02 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[conversations](
	[id] [uniqueidentifier] NOT NULL,
	[user_id] [uniqueidentifier] NOT NULL,
	[title] [nvarchar](300) NULL,
	[created_at] [datetime2](3) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[conversations] ADD  DEFAULT (newid()) FOR [id]
GO

ALTER TABLE [dbo].[conversations] ADD  DEFAULT (sysutcdatetime()) FOR [created_at]
GO

ALTER TABLE [dbo].[conversations]  WITH CHECK ADD  CONSTRAINT [FK_conversations_user] FOREIGN KEY([user_id])
REFERENCES [dbo].[users] ([id])
ON DELETE CASCADE
GO

ALTER TABLE [dbo].[conversations] CHECK CONSTRAINT [FK_conversations_user]
GO



USE [Smart_librarian_users]
GO

/****** Object:  Table [dbo].[recommendations]    Script Date: 10/16/2025 6:40:01 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[recommendations](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[conversation_id] [uniqueidentifier] NOT NULL,
	[book_title] [nvarchar](400) NOT NULL,
	[chroma_doc_id] [nvarchar](200) NULL,
	[reason] [nvarchar](max) NULL,
	[created_at] [datetime2](3) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[recommendations] ADD  DEFAULT (sysutcdatetime()) FOR [created_at]
GO

ALTER TABLE [dbo].[recommendations]  WITH CHECK ADD  CONSTRAINT [FK_recommendations_conversation] FOREIGN KEY([conversation_id])
REFERENCES [dbo].[conversations] ([id])
ON DELETE CASCADE
GO

ALTER TABLE [dbo].[recommendations] CHECK CONSTRAINT [FK_recommendations_conversation]
GO


USE [Smart_librarian_users]
GO

/****** Object:  Table [dbo].[settings]    Script Date: 10/16/2025 6:40:18 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[settings](
	[user_id] [uniqueidentifier] NOT NULL,
	[tts_enabled] [bit] NOT NULL,
	[stt_enabled] [bit] NOT NULL,
	[language] [nvarchar](20) NULL,
PRIMARY KEY CLUSTERED 
(
	[user_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[settings] ADD  DEFAULT ((0)) FOR [tts_enabled]
GO

ALTER TABLE [dbo].[settings] ADD  DEFAULT ((0)) FOR [stt_enabled]
GO

ALTER TABLE [dbo].[settings]  WITH CHECK ADD  CONSTRAINT [FK_settings_user] FOREIGN KEY([user_id])
REFERENCES [dbo].[users] ([id])
ON DELETE CASCADE
GO

ALTER TABLE [dbo].[settings] CHECK CONSTRAINT [FK_settings_user]
GO


USE [Smart_librarian_users]
GO

/****** Object:  Table [dbo].[users]    Script Date: 10/16/2025 6:40:34 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[users](
	[id] [uniqueidentifier] NOT NULL,
	[email] [nvarchar](320) NOT NULL,
	[name] [nvarchar](200) NULL,
	[password_hash] [varchar](255) NOT NULL,
	[role] [nvarchar](50) NOT NULL,
	[created_at] [datetime2](3) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[users] ADD  DEFAULT (newid()) FOR [id]
GO

ALTER TABLE [dbo].[users] ADD  DEFAULT ('user') FOR [role]
GO

ALTER TABLE [dbo].[users] ADD  DEFAULT (sysutcdatetime()) FOR [created_at]
GO


USE [Smart_librarian_users];
GO
SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

/* =========================================
   1) PLANURI & PREȚURI
   ========================================= */
CREATE TABLE dbo.billing_plans (
    id             INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_billing_plans PRIMARY KEY,
    code           NVARCHAR(50)  NOT NULL CONSTRAINT UQ_billing_plans_code UNIQUE,
    name           NVARCHAR(100) NOT NULL,
    period         VARCHAR(10)   NOT NULL CONSTRAINT DF_billing_plans_period DEFAULT ('month'), -- 'month'/'year'
    price_cents    INT           NOT NULL CONSTRAINT DF_billing_plans_price DEFAULT (0),
    currency       CHAR(3)       NOT NULL CONSTRAINT DF_billing_plans_currency DEFAULT ('EUR'),
    limits_json    NVARCHAR(MAX) NOT NULL,  -- ex: {"monthly_messages":1000,"tts":true}
    features_json  NVARCHAR(MAX) NOT NULL,
    is_active      BIT           NOT NULL CONSTRAINT DF_billing_plans_active DEFAULT (1),
    created_at     DATETIME2(3)  NOT NULL CONSTRAINT DF_billing_plans_created DEFAULT (sysutcdatetime())
);
GO

/* =========================================
   2) ABONAMENTE ACTIVE (FK user_id = UNIQUEIDENTIFIER)
   ========================================= */
CREATE TABLE dbo.subscriptions (
    id                     INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_subscriptions PRIMARY KEY,
    user_id                UNIQUEIDENTIFIER  NOT NULL
        CONSTRAINT FK_subscriptions_users REFERENCES dbo.users(id),
    plan_id                INT               NOT NULL
        CONSTRAINT FK_subscriptions_plans REFERENCES dbo.billing_plans(id),
    provider               NVARCHAR(30)      NOT NULL,  -- 'stripe', 'netopia', etc.
    provider_cust_id       NVARCHAR(100)     NULL,
    provider_sub_id        NVARCHAR(100)     NULL,
    status                 NVARCHAR(20)      NOT NULL,  -- 'trialing','active','past_due','canceled','incomplete'
    trial_end              DATETIME2(3)      NULL,
    current_period_start   DATETIME2(3)      NOT NULL,
    current_period_end     DATETIME2(3)      NOT NULL,
    cancel_at_period_end   BIT               NOT NULL CONSTRAINT DF_subscriptions_cancel DEFAULT (0),
    created_at             DATETIME2(3)      NOT NULL CONSTRAINT DF_subscriptions_created DEFAULT (sysutcdatetime())
);
GO

/* Un singur abonament trialing/active per user (index filtrat UNIQUE) */
CREATE UNIQUE INDEX UX_subscriptions_single_active
    ON dbo.subscriptions(user_id)
    WHERE status IN (N'trialing', N'active');
GO

/* Index uzual pentru interogări după user+status */
CREATE INDEX IX_subscriptions_user
    ON dbo.subscriptions(user_id, status);
GO

/* =========================================
   3) PLĂȚI / INVOICES
   ========================================= */
CREATE TABLE dbo.payments (
    id                    INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_payments PRIMARY KEY,
    user_id               UNIQUEIDENTIFIER  NOT NULL
        CONSTRAINT FK_payments_users REFERENCES dbo.users(id),
    subscription_id       INT               NULL
        CONSTRAINT FK_payments_subscriptions REFERENCES dbo.subscriptions(id),
    provider              NVARCHAR(30)      NOT NULL,         -- 'stripe', 'netopia', etc.
    provider_payment_id   NVARCHAR(100)     NOT NULL,         -- payment or invoice id
    amount_cents          INT               NOT NULL,
    currency              CHAR(3)           NOT NULL,
    status                NVARCHAR(20)      NOT NULL,         -- 'succeeded','failed','refunded'
    raw_payload           NVARCHAR(MAX)     NULL,             -- JSON webhook
    created_at            DATETIME2(3)      NOT NULL CONSTRAINT DF_payments_created DEFAULT (sysutcdatetime())
);
GO

CREATE INDEX IX_payments_user_created
    ON dbo.payments(user_id, created_at);
GO

/* =========================================
   4) CONSUM & QUOTA (lunar)
   ========================================= */
CREATE TABLE dbo.usage_counters (
    id             BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_usage_counters PRIMARY KEY,
    user_id        UNIQUEIDENTIFIER     NOT NULL
        CONSTRAINT FK_usage_users REFERENCES dbo.users(id),
    period_start   DATE                 NOT NULL,  -- prima zi a lunii
    period_end     DATE                 NOT NULL,  -- ultima zi a lunii
    messages_used  INT                  NOT NULL CONSTRAINT DF_usage_messages DEFAULT (0),
    tts_seconds    INT                  NOT NULL CONSTRAINT DF_usage_tts DEFAULT (0),
    stt_seconds    INT                  NOT NULL CONSTRAINT DF_usage_stt DEFAULT (0),
    last_update    DATETIME2(3)         NOT NULL CONSTRAINT DF_usage_last_update DEFAULT (sysutcdatetime()),
    CONSTRAINT UQ_usage_user_period UNIQUE (user_id, period_start, period_end)
);
GO

CREATE INDEX IX_usage_counters_user_period
    ON dbo.usage_counters(user_id, period_start);
GO

/* =========================================
   5) TRIAL GRATUIT
   ========================================= */
CREATE TABLE dbo.trials (
    user_id        UNIQUEIDENTIFIER NOT NULL
        CONSTRAINT PK_trials PRIMARY KEY
        CONSTRAINT FK_trials_users REFERENCES dbo.users(id),
    start_at       DATETIME2(3)     NOT NULL CONSTRAINT DF_trials_start DEFAULT (sysutcdatetime()),
    end_at         DATETIME2(3)     NULL,                -- setezi +7 zile la înscriere
    free_messages  INT              NOT NULL CONSTRAINT DF_trials_free DEFAULT (10),
    messages_used  INT              NOT NULL CONSTRAINT DF_trials_used DEFAULT (0)
);
GO

/* =========================================
   6) LOGURI DE BILLING (separate de logs generale)
   ========================================= */
CREATE TABLE dbo.billing_logs (
    id         BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_billing_logs PRIMARY KEY,
    user_id    UNIQUEIDENTIFIER     NULL
        CONSTRAINT FK_billing_logs_users REFERENCES dbo.users(id),
    action     NVARCHAR(100)        NOT NULL,  -- 'WEBHOOK_RECEIVED','QUOTA_BLOCK','METER_INCREMENT',...
    metadata   NVARCHAR(MAX)        NULL,      -- JSON
    created_at DATETIME2(3)         NOT NULL CONSTRAINT DF_billing_logs_created DEFAULT (sysutcdatetime())
);
GO


