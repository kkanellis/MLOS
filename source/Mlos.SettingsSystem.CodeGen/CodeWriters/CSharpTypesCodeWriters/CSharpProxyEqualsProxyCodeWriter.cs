// -----------------------------------------------------------------------
// <copyright file="CSharpProxyEqualsProxyCodeWriter.cs" company="Microsoft Corporation">
// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License. See LICENSE in the project root
// for license information.
// </copyright>
// -----------------------------------------------------------------------

using System;

using Mlos.SettingsSystem.Attributes;

namespace Mlos.SettingsSystem.CodeGen.CodeWriters.CSharpTypesCodeWriters
{
    /// <summary>
    /// Code writer class for CSharp ICodegenProxy implementation.
    /// </summary>
    /// <remarks>
    /// Writes all properties.
    /// </remarks>
    internal class CSharpProxyEqualsProxyCodeWriter : CSharpCodeWriter
    {
        /// <inheritdoc />
        public override bool Accept(Type sourceType) => sourceType.IsCodegenType();

        /// <inheritdoc />
        public override void WriteOpenTypeNamespace(string @namespace)
        {
            WriteLine($"namespace {Constants.ProxyNamespace}.{@namespace}");
            WriteLine("{");

            ++IndentationLevel;
        }

        /// <inheritdoc />
        public override void WriteCloseTypeNamespace(string @namespace)
        {
            --IndentationLevel;
            WriteLine($"}} // end namespace {Constants.ProxyNamespace}.{@namespace}");

            WriteLine();
        }

        /// <inheritdoc />
        public override void BeginVisitType(Type sourceType)
        {
            WriteOpenTypeDeclaration(sourceType.DeclaringType);

            string typeName = sourceType.Name;
            string typeFullName = $"global::{sourceType.GetTypeFullName()}";
            string proxyTypeFullName = $"{Constants.ProxyNamespace}.{sourceType.GetTypeFullName()}";

            WriteBlock($@"
                public partial struct {typeName}
                {{
                    /// <summary>
                    /// Operator ==.
                    /// </summary>
                    /// <param name=""left""></param>
                    /// <param name=""right""></param>
                    /// <returns></returns>
                    public static bool operator ==({proxyTypeFullName} left, {proxyTypeFullName} right) => left.Equals(right);

                    /// <summary>
                    /// Operator !=.
                    /// </summary>
                    /// <param name=""left""></param>
                    /// <param name=""right""></param>
                    /// <returns></returns>
                    public static bool operator !=({proxyTypeFullName} left, {proxyTypeFullName} right) => !(left == right);

                    /// <inheritdoc />
                    public override bool Equals(object obj)
                    {{
                        if (obj is {proxyTypeFullName})
                        {{
                            return Equals(({proxyTypeFullName})obj);
                        }}
                        else if (obj is {typeFullName})
                        {{
                            return Equals(({typeFullName})obj);
                        }}

                        return false;
                    }}

                    /// <inheritdoc />
                    public override int GetHashCode() => 0;

                    /// <inheritdoc/>
                    public bool Equals({proxyTypeFullName} other)
                    {{
                        bool result = true;");

            IndentationLevel += 2;
        }

        /// <inheritdoc/>
        public override void EndVisitType(Type sourceType)
        {
            WriteLine();
            WriteLine("return result;");
            IndentationLevel--;

            WriteLine("}");

            WriteCloseTypeDeclaration(sourceType);
        }

        /// <inheritdoc />
        public override void VisitField(CppField cppField)
        {
            string fieldName = cppField.FieldInfo.Name;

            WriteLine($"result &= this.{fieldName}.Equals(other.{fieldName});");
        }
    }
}
