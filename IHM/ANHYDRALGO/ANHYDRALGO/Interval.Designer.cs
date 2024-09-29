namespace ANHYDRALGO
{
    partial class DateScaleForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(DateScaleForm));
            this.numericUpDownMinimum = new System.Windows.Forms.NumericUpDown();
            this.numericUpDownMaximum = new System.Windows.Forms.NumericUpDown();
            this.OKButtonDateForm = new System.Windows.Forms.Button();
            this.CancelButtonDateForm = new System.Windows.Forms.Button();
            this.MinimumDateLabel = new System.Windows.Forms.Label();
            this.MaximumDateLabel = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownMinimum)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownMaximum)).BeginInit();
            this.SuspendLayout();
            // 
            // numericUpDownMinimum
            // 
            this.numericUpDownMinimum.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.numericUpDownMinimum.Font = new System.Drawing.Font("Gill Sans Ultra Bold", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.numericUpDownMinimum.Location = new System.Drawing.Point(135, 35);
            this.numericUpDownMinimum.Maximum = new decimal(new int[] {
            2024,
            0,
            0,
            0});
            this.numericUpDownMinimum.Minimum = new decimal(new int[] {
            1990,
            0,
            0,
            0});
            this.numericUpDownMinimum.Name = "numericUpDownMinimum";
            this.numericUpDownMinimum.Size = new System.Drawing.Size(66, 17);
            this.numericUpDownMinimum.TabIndex = 0;
            this.numericUpDownMinimum.Value = new decimal(new int[] {
            1990,
            0,
            0,
            0});
            this.numericUpDownMinimum.ValueChanged += new System.EventHandler(this.NumericUpDownMin_ValueChanged);
            // 
            // numericUpDownMaximum
            // 
            this.numericUpDownMaximum.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.numericUpDownMaximum.Font = new System.Drawing.Font("Gill Sans Ultra Bold", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.numericUpDownMaximum.Location = new System.Drawing.Point(135, 71);
            this.numericUpDownMaximum.Maximum = new decimal(new int[] {
            2024,
            0,
            0,
            0});
            this.numericUpDownMaximum.Minimum = new decimal(new int[] {
            1990,
            0,
            0,
            0});
            this.numericUpDownMaximum.Name = "numericUpDownMaximum";
            this.numericUpDownMaximum.Size = new System.Drawing.Size(66, 17);
            this.numericUpDownMaximum.TabIndex = 1;
            this.numericUpDownMaximum.Value = new decimal(new int[] {
            2024,
            0,
            0,
            0});
            this.numericUpDownMaximum.ValueChanged += new System.EventHandler(this.NumericUpDownMax_ValueChanged);
            // 
            // OKButtonDateForm
            // 
            this.OKButtonDateForm.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(116)))), ((int)(((byte)(180)))), ((int)(((byte)(76)))));
            this.OKButtonDateForm.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.OKButtonDateForm.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(116)))), ((int)(((byte)(180)))), ((int)(((byte)(76)))));
            this.OKButtonDateForm.FlatAppearance.BorderSize = 0;
            this.OKButtonDateForm.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.OKButtonDateForm.Font = new System.Drawing.Font("Gill Sans Ultra Bold Condensed", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.OKButtonDateForm.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.OKButtonDateForm.Location = new System.Drawing.Point(135, 105);
            this.OKButtonDateForm.Name = "OKButtonDateForm";
            this.OKButtonDateForm.Size = new System.Drawing.Size(96, 31);
            this.OKButtonDateForm.TabIndex = 27;
            this.OKButtonDateForm.Text = "OK";
            this.OKButtonDateForm.UseVisualStyleBackColor = false;
            // 
            // CancelButtonDateForm
            // 
            this.CancelButtonDateForm.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(116)))), ((int)(((byte)(180)))), ((int)(((byte)(76)))));
            this.CancelButtonDateForm.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.CancelButtonDateForm.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(116)))), ((int)(((byte)(180)))), ((int)(((byte)(76)))));
            this.CancelButtonDateForm.FlatAppearance.BorderSize = 0;
            this.CancelButtonDateForm.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.CancelButtonDateForm.Font = new System.Drawing.Font("Gill Sans Ultra Bold Condensed", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.CancelButtonDateForm.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.CancelButtonDateForm.Location = new System.Drawing.Point(12, 105);
            this.CancelButtonDateForm.Name = "CancelButtonDateForm";
            this.CancelButtonDateForm.Size = new System.Drawing.Size(96, 31);
            this.CancelButtonDateForm.TabIndex = 28;
            this.CancelButtonDateForm.Text = "Cancel";
            this.CancelButtonDateForm.UseVisualStyleBackColor = false;
            // 
            // MinimumDateLabel
            // 
            this.MinimumDateLabel.AutoSize = true;
            this.MinimumDateLabel.BackColor = System.Drawing.Color.Transparent;
            this.MinimumDateLabel.Font = new System.Drawing.Font("Gill Sans Ultra Bold Condensed", 10.15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.MinimumDateLabel.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.MinimumDateLabel.Location = new System.Drawing.Point(43, 35);
            this.MinimumDateLabel.Name = "MinimumDateLabel";
            this.MinimumDateLabel.Size = new System.Drawing.Size(65, 19);
            this.MinimumDateLabel.TabIndex = 29;
            this.MinimumDateLabel.Text = "MINIMUM";
            // 
            // MaximumDateLabel
            // 
            this.MaximumDateLabel.AutoSize = true;
            this.MaximumDateLabel.BackColor = System.Drawing.Color.Transparent;
            this.MaximumDateLabel.Font = new System.Drawing.Font("Gill Sans Ultra Bold Condensed", 10.15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.MaximumDateLabel.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.MaximumDateLabel.Location = new System.Drawing.Point(38, 72);
            this.MaximumDateLabel.Name = "MaximumDateLabel";
            this.MaximumDateLabel.Size = new System.Drawing.Size(70, 19);
            this.MaximumDateLabel.TabIndex = 30;
            this.MaximumDateLabel.Text = "MAXIMUM";
            // 
            // DateScaleForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.ClientSize = new System.Drawing.Size(243, 148);
            this.Controls.Add(this.MaximumDateLabel);
            this.Controls.Add(this.MinimumDateLabel);
            this.Controls.Add(this.CancelButtonDateForm);
            this.Controls.Add(this.OKButtonDateForm);
            this.Controls.Add(this.numericUpDownMaximum);
            this.Controls.Add(this.numericUpDownMinimum);
            this.Name = "DateScaleForm";
            this.Text = "Choose the interval";
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownMinimum)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownMaximum)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.NumericUpDown numericUpDownMinimum;
        private System.Windows.Forms.NumericUpDown numericUpDownMaximum;
        private System.Windows.Forms.Button OKButtonDateForm;
        private System.Windows.Forms.Button CancelButtonDateForm;
        private System.Windows.Forms.Label MinimumDateLabel;
        private System.Windows.Forms.Label MaximumDateLabel;
    }
}